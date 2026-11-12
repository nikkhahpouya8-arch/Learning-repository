from Test_Database import get_due_early_reminders, get_due_final_reminders

def get_reminders_to_notify(current_time):
    
    due_early_reminders = get_due_early_reminders(current_time)
    
    due_final_reminders = get_due_final_reminders(current_time)
    
    return due_early_reminders, due_final_reminders

