# -*- coding: utf-8 -*-
# try something like
import datetime
import getpass

# Global dictionary for all status options and their colors
STATUS_COLOR = {"Not started" : "#0000fe",
                "WIP" : "#c9a87d",
                "Need Fixing" : "#83a0c2",
                "Failed QA" : "#f90105",
                "Rendered" : "#f9e205",
                "Done" : "#f9b6fc",
                "Deleted" : "#bcc692"}

def index(): return dict(message="hello from shots.py")

def get_status_options():
    """
    Return the global dictionary.
    Implemented in order to be able to get this dictionary from others modules.
    """
    return STATUS_COLOR

def status():
    """
    Main function which communicates with the main view.
    """
    status_colors = get_status_options() # set the global dictionary in local variable

    # check which shot (entry) should be displayed
    if request.args(0) is None:
        # default
        row_to_display = db(db.shots).select().first()
    else:
        id = request.args(0)
        row_to_display = db.shots(db.shots.id == id)

    # get and set the variables from the form
    if request.post_vars:
        # get current date and user
        now = datetime.datetime.now()
        user = getpass.getuser()

        # validate if Name is not empty
        if name_is_empty(request.post_vars.Name):
            response.flash = T('You cannot add shot with empty name!')
            rows = db(db.shots).select(orderby=db.shots.Name)
            return locals()

        # validate if Number of Frames is integer
        if not number_of_frames_is_int(request.post_vars.Number_of_Frames):
            response.flash = T('You must insert a positive value in Number of Frames field!')
            rows = db(db.shots).select(orderby=db.shots.Name)
            return locals()

        # check if we need to create new shot or update exist shot based on shot's name in form
        if db(db.shots.Name == request.post_vars.Name).select().first():
            update_record(now, user)
        else:
            add_record(now, user)

        # update the row to display according to user's select
        row_to_display = db.shots(db.shots.Name == request.post_vars.Name)

    # get the updated rows from db
    rows = db(db.shots).select(orderby=db.shots.Name)
    return locals()

def add_record(current_time, user):
    """
    Add new shot record into local db.
    Triggered when new shot's name specified in form.
    """
    db.shots.insert(Name = request.post_vars.Name, Number_of_Frames = request.post_vars.Number_of_Frames, Modified_Date = current_time, Modified_By = user, Status = request.post_vars.Status, Is_Active = request.post_vars.Is_Active, Description = request.post_vars.Description)
    response.flash = T('The record was added successfully')

def update_record(current_time, user):
    """
    Update shot record in local db.
    Triggered when exist shot's name specified in form.
    """
    db(db.shots.Name == request.post_vars.Name).update(Number_of_Frames = request.post_vars.Number_of_Frames, Modified_Date = current_time, Modified_By = user, Status = request.post_vars.Status, Is_Active = request.post_vars.Is_Active, Description = request.post_vars.Description)
    response.flash = T('The record updated successfully')

def name_is_empty(input):
    """
    Validate Name input.
    """
    if not input:
        return True
    return False

def number_of_frames_is_int(input):
    """
    Validate Number of Frame input.
    """
    try:
        int(input)
        return True
    except ValueError:
        return False
