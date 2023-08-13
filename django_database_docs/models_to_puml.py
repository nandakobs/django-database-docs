import os
import sys

import django
from django.apps import apps
from django.db.models import (
    AutoField, BigIntegerField, BinaryField, BooleanField, CharField,
    DateField, DateTimeField, DecimalField, DurationField, EmailField, FloatField, IntegerField,
    IPAddressField, GenericIPAddressField, NullBooleanField, PositiveIntegerField,
    PositiveSmallIntegerField, SlugField, SmallIntegerField, TextField,
    TimeField, URLField, UUIDField, Field, FileField, ForeignKey, ImageField, OneToOneField, ManyToManyField, JSONField,
)


def get_project_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    django_dir = os.path.dirname(current_dir)
    project_dir = os.path.dirname(django_dir)

    return project_dir


def get_project_name():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_name = os.path.basename(os.path.dirname(current_dir))
    return project_name


sys.path.append(get_project_path())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{get_project_name()}.settings')
django.setup()
models = apps.get_models()


def make_output_file_editable(file_path):
    """
    In some projects, the generated file is created with the read-only permission.
    This method makes sure the output file is editable.
    """
    permissions = 0o777  # 777 (octal) means read, write, and execute permissions for the owner, group, and others
    os.chmod(file_path, permissions)


def django_field_to_postgres(field) -> str:
    mapping = {
        AutoField: "serial",
        BigIntegerField: "bigint",
        BinaryField: "bytea",
        BooleanField: "boolean",
        CharField: f"varchar({field.max_length})",
        DateField: "date",
        DateTimeField: "timestamp with time zone",
        DecimalField: f"numeric({field.max_digits},{field.decimal_places})" if hasattr(field, "max_digits") and hasattr(
            field, "decimal_places") else "numeric",
        DurationField: "interval",
        EmailField: "varchar(254)",
        FileField: "varchar(100)",
        FloatField: "double precision",
        ImageField: "varchar(100)",
        IntegerField: "integer",
        IPAddressField: "inet",
        GenericIPAddressField: "inet",
        NullBooleanField: "boolean",
        PositiveIntegerField: "integer",
        PositiveSmallIntegerField: "smallint",
        SlugField: "varchar(50)",
        SmallIntegerField: "smallint",
        TextField: "text",
        TimeField: "time",
        URLField: "varchar(200)",
        UUIDField: "uuid",
        JSONField: "jsonb",
        OneToOneField: "uuid",  # Assumes uuid as a primary key
    }

    return mapping.get(type(field), "undefined")


def generate_many_to_many_field(field):
    app_label = field.model._meta.app_label
    model_name = field.model.__name__
    related_app_label = field.related_model._meta.app_label
    related_model_name = field.related_model.__name__

    intermediate_table_name = f"{app_label}_{model_name}_{related_app_label}_{related_model_name}"

    # fk fields for both related models
    model_fk_field = f"{model_name}_id: integer"
    related_model_fk_field = f"{related_model_name}_id: integer"

    # id field for the relationship
    m2m_id = "id: integer"

    return intermediate_table_name, [model_fk_field, related_model_fk_field, m2m_id]


def get_target_table(field):
    target_table = field.related_model._meta.label
    return target_table.replace(".", "_")


def generate_puml_file(output_file, models):
    with open(output_file, "w") as f:
        f.write("@startuml\n\n")
        f.write("!theme plain\ntop to bottom direction\nskinparam linetype ortho\n\n")

        m2m_tables = []
        m2m_relationships = []
        fk_relationships = []

        for model in models:
            app_name = model._meta.app_label
            model_name = model.__name__
            f.write(f"class {app_name}_{model_name.lower()} {{\n")

            for field in model._meta.get_fields():
                if isinstance(field, Field):
                    if isinstance(field, ManyToManyField):
                        intermediate_table_name, fk_fields = generate_many_to_many_field(field)
                        m2m_tables.append((intermediate_table_name, fk_fields))
                        m2m_relationships.append(
                            (f"{intermediate_table_name}", get_target_table(field), f"{field.name}_id")
                        )
                    elif isinstance(field, ForeignKey):
                        fk_name = f"{field.name}_id"
                        fk_relationships.append((f"{app_name}_{model_name}", get_target_table(field), fk_name))
                        f.write(f"  {fk_name}: uuid\n")
                    else:
                        field_type = django_field_to_postgres(field)
                        f.write(f"  {field.name}: {field_type}\n")

            f.write("}\n")

        for m2m_table, fk_fields in m2m_tables:
            f.write(f"class {m2m_table.lower()} {{\n")
            for fk_field in fk_fields:
                f.write(f"  {fk_field}\n")
            f.write("}\n")

        for source_table, target_table, fk_name in fk_relationships:
            f.write(f"{source_table.lower()} -[#595959,plain]-^ {target_table.lower()} : {fk_name.lower()}:id\n")

        for source_table, target_table, m2m_name in m2m_relationships:
            f.write(f"{source_table.lower()} -[#595959,dashed]- {target_table.lower()} : {m2m_name.lower()}:id\n")

        f.write("\n@enduml\n")


generate_puml_file("result.puml", models)
make_output_file_editable("./result.puml")
