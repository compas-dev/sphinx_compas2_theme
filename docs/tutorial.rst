********************************************************************************
Tutorial
********************************************************************************

Basic Structure
===============

sidebaronly
-----------

multisection
------------


Add a Custom ``autosummary`` Template
=====================================

In the ``conf.py`` file, add the path to your local templates folder.
The path should be relative to the ``docs`` folder.

.. code-block:: python

    templates_path = sphinx_compas2_theme.get_autosummary_templates_path()
    templates_path += ['_templates']

In the ``_templates`` folder, add as many custom ``autosummary`` templates as you want.
The name of the file is the name of the template.

For example, to add a custom template for the ``autosummary`` of a ``class`` object that excludes inherited methods,
add ``class_noinheritance.rst``.

.. code-block:: rst

    {{ objname | escape | underline }}

    .. currentmodule:: {{ module }}

    .. autoclass:: {{ objname }}

        {% block methods %}
        .. rubric:: Methods

        .. autosummary::
            :toctree:
            :nosignatures:
        {% for item in methods %}
        {% if item not in inherited_members %}
            ~{{ name }}.{{ item }}
        {% endif %}
        {%- endfor %}

        {% endblock %}

Finally, tell ``autosummary`` to use the custom template.

.. code-block:: rst

    .. autosummary::
        :toctree: generated/
        :nosignatures:
        :template: class_noinheritance.rst
