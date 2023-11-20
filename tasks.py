from background_task import background

@background(schedule=10)  # Schedule the task to run every 60 seconds
def my_scheduled_task():
    # Your task code goes here
    print("Executing scheduled task now...")
    # This function will be executed at the scheduled time