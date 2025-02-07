from sqladmin import ModelView
from .models import Skills

class SkillAdmin(ModelView, model=Skills):
    column_list = [Skills.id, Skills.title, Skills.description]
    column_searchable_list = [Skills.title]
    column_sortable_list = [Skills.id, Skills.title]
