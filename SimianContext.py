"""Simian Python LLM context file.

Advise:
* Logic to hide or disable components reduces performance.
* More components means more information to process, resulting in slower performance.
* The same applies to the amount of data.
* Reusing components WITH functionality is possible via composedComponents.
"""

import os
from typing import Union

from simian.gui import Form, component, component_properties
import simian.gui.utils as utils


if __name__ == "__main__":
    # Run the Simian web app in a local pywebview browser.
    from simian.local import Uiformio

    Uiformio("SimianContext", window_title="Simian Web App", debug=False, show_refresh=True)


def gui_init(meta_data: dict) -> dict:
    """Initialize the zoo_ui app."""
    # Register component initialization functions.
    Form.componentInitializer(
        componentKey=component_initializer_function,
        otherComponentKey=other_component_initializer_function,
    )

    # Create the form and load the json definition from the builder into it.
    form_obj = Form(from_file=__file__)

    comp = component.Button(key="ComponentKey", parent=form_obj)
    comp.label = "Click me"
    comp.setEvent(event_name="EventName")

    return {
        "form": form_obj,
        "navbar": {
            "title": "Simian demo",
            "logo": utils.encodeImage(
                os.path.join(os.path.dirname(__file__), "logo_tasti_light.png")
            ),
        },
    }


def component_initializer_function(comp: component.Component) -> None:
    """Component initializer function."""
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


def component_initializer_value_change(comp: component.Component) -> None:
    """Make a component fire a "change" event when its value is changed."""
    comp.properties = {"triggerHappy": True}  # No setEvent(). Fires event "change".


def component_initializer_value_change_named(comp: component.Component) -> None:
    """Make a component fire a named event when its value is changed."""
    comp.properties = {"triggerHappy": "SpecificValueChangedEvent"}  # No setEvent().


def component_initializer_focuslost(comp: component.Component) -> None:
    """Make a component fire an event when it loses focus."""
    comp.customClass = "EventOnBlur"  # No setEvent(). Fires event "blur".


def other_component_initializer_function(comp: component.Component) -> None:
    """Other component initializer function."""
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


def event_callback_function(meta_data: dict, payload: dict) -> dict:
    """EventName callback function.

    Args:
        meta_data:      Form meta data.
        payload:        Current status of the Form's contents.

    Returns:
        payload:        Updated Form contents.
    """
    old_value, _ = utils.getSubmissionData(payload=payload, key="ComponentKey")
    new_value = old_value + 2
    utils.setSubmissionData(payload=payload, key="ComponentKey", data=new_value)
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
