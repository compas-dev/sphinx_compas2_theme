{% set methods_proper = [] %}
{% set methods_inherited = [] %}
{% for item in methods %}
    {% if item not in inherited_members %}
        {% set result = methods_proper.append(item) %}
    {% else %}
        {% set result = methods_inherited.append(item) %}
    {% endif %}
{% endfor %}

{{ objname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

    {% block methods %}
    {% if methods_proper %}
    .. rubric:: Methods

    .. autosummary::
        :toctree:
        :nosignatures:
    {% for item in methods_proper %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}

    {% if methods_inherited %}
    .. rubric:: Inherited Methods

    .. autosummary::
        :toctree:
        :nosignatures:
    {% for item in methods_inherited %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}

    {% endblock %}
