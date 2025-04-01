"""Simian Python LLM context file.

Advise:
* Logic to hide or disable components reduces performance.
* More components means more information to process, resulting in slower performance.
* The same applies to the amount of data.
* Reusing components WITH functionality is possible via composedComponents.
"""

import os
from typing import Union

from simian.gui import Form, component, component_properties, composed_component
import simian.gui.utils as utils


if __name__ == "__main__":
    # Run the Simian web app in a local pywebview browser.
    from simian.local import Uiformio

    Uiformio("SimianContext", window_title="Simian Web App", debug=False, show_refresh=True)


def gui_init(meta_data: dict) -> dict:
    """Initialize the zoo_ui app."""
    # Register component initialization functions to modify the properties of existing components.
    Form.componentInitializer(
        componentKey=component_initializer_function,
        otherComponentKey=other_component_initializer_function,
        DataTablesComponentKey=component_initializer_datatables,
        PlotlyKey=component_initializer_plotly,
        propertyEditorKey=composed_component.PropertyEditor.get_initializer(
            default_value=composed_component.PropertyEditor.prepare_values([], []),
            column_label="Properties",
            allow_editing=True,  # Set to false to make it a PropertyViewer.
        ),
    )

    # Create the form and load the json definition from the builder into it.
    form_obj = Form(from_file=__file__)

    # New components must be explicitly added to the form using their constructor.
    # Add a new Button component to the form with a click event "EventName".
    comp = component.Button(key="runButton", parent=form_obj)
    comp.label = "Click me"
    comp.setEvent(event_name="EventName")

    # Composed components need a parent 'Composed'. Properties are set via a component initializer.
    comp = component.Composed(key="propertyEditorKey", parent=form_obj)
    comp.className = "simian.gui.composed_component.PropertyEditor"

    return {
        "form": form_obj,
        "navbar": {
            "title": "Simian demo",
            "logo": utils.encodeImage(
                os.path.join(os.path.dirname(__file__), "logo_tasti_light.png")
            ),
        },
    }


def gui_event(meta_data: dict, payload: dict) -> dict:
    """Simian Web App callback routing function.

    Args:
        meta_data:      Form meta data.
        payload:        Current status of the Form's contents.

    Returns:
        payload:        Updated Form contents.
    """
    # Register our event callbacks to the events.
    Form.eventHandler(
        EventName=event_callback_function,
        blur=blur_function,
        SpecificValueChangedEvent=specific_value_changed,
        change=ValueChangedEvent,
    )

    # Execute the callback.
    callback = utils.getEventFunction(meta_data, payload)
    return callback(meta_data, payload)


def component_initializer_function(comp: component.Component) -> None:
    """Component initializer function to change the properties of an existing component."""
    comp.label = "New label"
    comp.description = "Component description"
    comp.tooltip = "Component tooltip"
    comp.labelPosition = "left-left"
    comp.hideLabel = True
    comp.hidden = True
    comp.defaultValue = 2  # initial data.
    comp.placeholder = 1
    comp.calculateValue = "value = data.otherComponentKey + 2;"
    comp.disabled = True
    comp.customClass = "bootstrap-class"
    comp.customClass = (
        "form-check-inline"  # Components with this customClass are put next to eachother
    )
    comp.attributes = {"style": "color:red"}  # add HTML attributes to the component.

    # Enabling / Disabling:
    comp.disable_when(
        trigger_type="simple", trigger_value={"OtherComponentKey", 2}, disable_component=True
    )  # Simple syntax to disable the component when OtherComponentKey is 2.
    comp.disable_when(
        trigger_type="result", trigger_value="data.otherComponentKey == 2;", disable_component=True
    )  # Alternative syntax with a custom javascript expression.
    comp.disable_when(
        trigger_type="event", trigger_value="EventName", disable_component=True
    )  # Syntax with an event EventName trigger.

    # Hide the component when the value of OtherComponentKey equals 2.
    cond = component_properties.Conditional(parent=comp)
    cond.show = False
    cond.when = "otherComponentKey"
    cond.eq = 2  # Does not contain gt, lt, ge, le.

    # Hide the component when the value of OtherComponentKey equals 2. Javascript expression.
    comp.customConditional("show = !(data.otherComponentKey == 2);")
    # Show the component when the value of OtherComponentKey equals 2. Javascript expression.
    comp.customConditional("show = data.otherComponentKey == 2;")

    # Validation:
    comp.add_validation(
        required=True,  # Value may not be empty.
        min=2,  # Value must be at least 2.
        max=10,  # Value must be at most 10.
        integer=True,  # Value must be an integer.
        minLength=3,  # Minimum length of a text value.
        maxLength=5,  # Maximum length of a text value.
        minWords=2,  # Minimum number of words in a text value.
        maxWords=5,  # Maximum number of words in a text value.
        pattern=".*",  # Regular expression pattern.
        custom="valid = data.otherComponentKey + 2 > 3;",  # Custom javascript validation function.
        customMessage="Value must be between 2 and 10",  # Overrides specific validation error messages.
    )

    # Add specific error messages for validation with string interpolations.
    error = component_properties.Error(parent=comp)
    error.required = "Value of {{ field }} may not be empty."
    error.min = "Value of {{ field }} must be at least {{ min }}."
    error.max = "Value of {{ field }} must be at most {{ max }}."
    error.minLength = "Value of {{ field }} must have at least {{ length }} characters."
    error.maxLength = "Value of {{ field }} must have at most {{ length }} characters."
    error.invalid_email = "Value of {{ field }} must be a valid email address."
    error.invalid_date = "Value of {{ field }} must be a valid date."
    error.pattern = "Value of {{ field }} must match the pattern {{ pattern }}."
    error.custom = "Value of {{ field }} is invalid."  # Error message for custom validation.


def component_initializer_datatables(comp: component.DataTables):
    """Set the columns of an existing DataTables component."""
    # A DataTables component must have a first column "id".
    comp.setColumns(  # Must contain column "id'!"
        titles=["id"],  # must contain "id"!
        keys=["id"],  # must contain "id"!
        visible=[False],  # Always hide the "id" column!
    )

    comp.setColumns(  # Must contain column "id'!"
        titles=["id", "Name", "Age", "Present"],  # must contain "id"!
        keys=["id", "name", "age", "present"],  # must contain "id"!
        visible=[False, True, True, True],  # Always hide the "id" column!
        orderable=[False, True, False, False],  # Option for sorting columns.
        searchable=[False, True, False, True],  # Option for searching columns.
        # Columns with className 'text-muted' are not editable.
        className=["text-muted", "text-muted", None, "text-muted"],  # Option for disabling columns
    )

    # Add default values to the DataTables component with two rows. The "id" column must contain unique values.
    comp.defaultValue = [
        {"id": 0, "name": "Bob", "age": 49, "present": True},
        {"id": 1, "name": "Sarah", "age": 47, "present": False},
    ]


def component_initializer_datatables_options(comp: component.DataTables):
    # Options to change default features of the DataTables component.
    comp.setFeatures(
        searching=False,  # Option to disable search in table.
        ordering=False,  # Option to prevent column sorting.
        paging=False,  # Option to prevent pagination.
        deferRender=True,  # Option to render one table page at a time to improve performance.
    )

    comp.setOptions(
        pageLength=30,  # Option to set the initial table pagination length.
        lengthMenu=[10, 30, {"label": "All", "value": -1}],  # Option to set pagination length menu
        order=[[1, "asc"], [0, "desc"]],  # Option to set default column sorting.
    )

    comp.setInternationalisation(
        decimal=".",  # Option to set the decimal separator.
        thousands=",",  # Option to set the thousands separator.
    )


def datatables_callback(meta_data: dict, payload: dict):
    """Update the contents of a DataTables component."""
    table_value, _ = utils.getSubmissionData(payload, key="datatables_key")

    # Append the datatables contents with an extra row. The id must be unique!
    table_value.append({"id": 2, "name": "Sarah", "age": 47, "present": False})

    utils.setSubmissionData(payload, key="datatables_key", data=table_value)

    return payload


def component_initializer_plotly(comp: component.Plotly):
    """Initialize a Plotly component."""
    comp.aspectRatio = 4 / 3  # Ratio between width and height of the figure.

    # Add an initial plot using the plotly graphics library.
    import plotly.graph_objects as go

    comp.figure = go.Figure()

    # Reduce the margin around the plot area.
    comp.figure.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})

    # Allow drawing shapes in the plotly axes:
    comp.figure.update_layout(
        dragmode="drawclosedpath",  # Draw a closed path on a mouse drag
        newshape_line_color="white",
        newshape_fillcolor="white",
        newshape_fillrule="nonzero",  # Shape is completely filled. "evenodd" (default) for cut-outs
    )

    comp.defaultValue["config"].update(
        {
            "modeBarButtonsToAdd": [  # Add extra edit options to the Plotly component.
                "drawclosedpath",
                "drawcircle",
                "drawrect",
                "eraseshape",  # Add button to remove shapes.
            ]
        }
    )


def process_plotly_callback(meta_data: dict, payload: dict):
    """Update the plotly component contents in a callback function."""
    plot_obj, _ = utils.getSubmissionData(payload, key="plotly")
    plot_obj.figure.add_scatter(
        x=[1, 2, 3, 4, 5],
        y=[0.35, 0.95, 0.32, 0.54, 0.23],
    )
    payload, _ = utils.setSubmissionData(payload, "plotly", plot_obj)

    return payload


def process_plotly_clear(meta_data: dict, payload: dict):
    """Clear the contents of the plotly component in a callback function."""
    plot_obj, _ = utils.getSubmissionData(payload, key="plotly")
    plot_obj.clearFigure(keepLayout=True)
    payload, _ = utils.setSubmissionData(payload, "plotly", plot_obj)

    return payload


def process_plotly_shapes(meta_data: dict, payload: dict):
    """Process shapes drawn in the plotly component and add some more."""
    plot_obj, _ = utils.getSubmissionData(payload, key="plotly")
    shapes_list_of_dicts = plot_obj.getShapes()  # Get all existing shapes.
    plot_obj.layout["shapes"] = []  # Remove all existing shapes.

    simple_shape_box = {
        "type": "line",  # May also be "rect" (for rectangle) and "circle"
        "x": [20, 30],  # x-coordinates of the bounding box.
        "y": [15, 25],  # y-coordinates of the bounding box.
    }
    plot_obj.addShape(simple_shape_box)

    path_shape = {
        "type": "path",  # Polygon
        "x": [20, 30, 25],  # x-coordinates of the vertices
        "y": [15, 25, 30],  # y-coordinates of the vertices
        "closed": True,  # Closed polygon
    }
    plot_obj.addShape(path_shape)
    utils.setSubmissionData(payload, key="plotly", data=plot_obj)
    return payload


def component_initializer_plotly_background(comp: component.Plotly):
    """Show a background image in the Plotly component."""
    import plotly.graph_objects as go

    comp.figure = go.Figure()  # Add an initial plot using the plotly graphics library.

    # Adding a background image
    selected_image_file = "background.png"
    base64_image = utils.encodeImage(selected_image_file)
    img_width = 600
    img_height = 300

    image_setup = [
        {
            "source": base64_image,
            "xref": "x",
            "yref": "y",
            "xanchor": "left",
            "yanchor": "top",
            "x": 1,
            "y": 1,
            "sizex": img_width,
            "sizey": img_height,
            "layer": "below",
        }
    ]

    comp.figure.update_layout(images=image_setup, margin={"l": 0, "r": 0, "t": 0, "b": 0})
    comp.figure.update_xaxes(showgrid=False, range=(1, img_width + 1))
    comp.figure.update_yaxes(showgrid=False, scaleanchor="x", range=(img_height + 1, 1))


def component_initializer_value_change(comp: component.Component) -> None:
    """Make an existing component fire a "change" event when its value is changed."""
    comp.properties = {"triggerHappy": True}  # No setEvent(). Fires event "change".


def component_initializer_value_change_named(comp: component.Component) -> None:
    """Make an existing component fire a named event when its value is changed."""
    comp.properties = {"triggerHappy": "SpecificValueChangedEvent"}  # No setEvent().


def component_initializer_focuslost(comp: component.Component) -> None:
    """Make an existing component fire an event when it loses focus."""
    comp.customClass = "EventOnBlur"  # No setEvent(). Fires event "blur".


def other_component_initializer_function(comp: component.Component) -> None:
    """Other existing component initializer function."""
    comp.label = "Other component label"


def initializer_function_dynamic_options(comp: component.Select) -> None:
    """Fill Select component with options using the value of another component."""
    comp.dataSrc = "custom"
    comp.data = {"custom": "values = data.otherComponentKey;"}


def add_component(
    base: Union[
        component.Container,
        component.FieldSet,
        component.Panel,
        component.Table,
        component.Well,
        component.EditGrid,
        component.DataGrid,
    ],
    comp: component.Component,
) -> None:
    """Put a component in another component that can contain components."""
    base.addComponent(comp)


def event_callback_function(meta_data: dict, payload: dict) -> dict:
    """EventName callback function.

    Args:
        meta_data:      Form meta data.
        payload:        Current status of the Form's contents.

    Returns:
        payload:        Updated Form contents.
    """
    # Generic component value updating.
    old_value, _ = utils.getSubmissionData(payload=payload, key="ComponentKey")
    new_value = old_value + 2
    utils.setSubmissionData(payload=payload, key="ComponentKey", data=new_value)

    # PropertyEditor specific value updating.
    property_editor_rows = [
        {
            "datatype": "text", # Or "boolean", "numeric", "select"
            "label": "Property name",           # Mandatory
            "tooltip": "Tooltip text",
            "required": False,
            "defaultValue": "Default value",    # Defaults to a minLength long list of Nones.
            "min": 0,                           # "numeric"
            "max": 2,                           # "numeric"
            "decimalLimit": 2,                  # "numeric"
            "allowed": [],                      # "select" component data source values definition.
            "minLength": 1,                     # {1} Scalar, or minimum array length of 0 or more.
            "maxLength": 1,                     # {1} Scalar, or maximum array length of 0 or more.
        }
    ]  # fmt: skip

    new_props = composed_component.PropertyEditor.prepare_values(
        prop_meta=property_editor_rows,
        prop_values=["New value"],
    )
    utils.setSubmissionData(payload=payload, key="propertyEditorKey", data=new_props)

    # Get PropertyEditor values.
    props, _ = utils.getSubmissionData(payload=payload, key="propertyEditorKey")
    prop_values = composed_component.PropertyEditor.get_values(props)

    utils.addAlert(
        payload,
        message="Event message to show",
        type="info",  # Type of alert: "info", "success", "warning", "danger"
    )

    return payload


def blur_function(meta_data: dict, payload: dict) -> dict:
    """EventOnBlur ("blur") callback function."""
    if payload["key"] == "ComponentKey":
        # Do something
        pass
    return payload


def ValueChangedEvent(meta_data: dict, payload: dict) -> dict:
    """ValueChangedEvent callback function."""
    if payload["key"] == "ComponentKey":
        # Do something when the value of "ComponentKey" is changed.
        pass

    return payload


def specific_value_changed(meta_data: dict, payload: dict) -> dict:
    """ValueChangedEvent callback function."""
    # Do something when the value of the triggerHappy component is changed.

    # Fire the EventName event after this event.
    payload["followUp"] = "EventName"
    return payload
