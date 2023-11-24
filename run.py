
import pyautogui
from pynput import keyboard

import time
import threading


start_time = 10      # How long to wait before script starts

# Wait timers, I tried to set it as low as possible to make it faster
# you can increase it if there are difficulties executing the script
wait_time = 1.3     # How long to wait each code entered
char_time = 0.1     # Appropriately adds additional time to wait_time for longer codes typing







with open('codes.txt', 'r') as file:
    codes = [line.strip() for line in file.readlines()]


char_count = 0
for code in codes:
    char_count += len(code)

total_time = start_time + wait_time*len(codes) + char_count*char_time*2
mins, secs = divmod( total_time, 60 )
print( f'Promo Code count: {len(codes)}' )
print( f'Estimated execution time: {int(mins)}m {int(secs)}s' )
print( '(Maybe a little longer, pyautogui typing is a bit slow for some reason.)' )
print( '-----' )



def countdown_before_start( sec ):
    while sec:
        print( f'Start in {sec} seconds' )
        time.sleep( 1 )
        sec -= 1
countdown_before_start(start_time)

cursor = pyautogui.position()
exiting = False

def input_loop():
    global exiting
    
    count = 0
    for code in codes:
        
        if exiting:
            return False
        
        count += 1
        print( f'{count} - {code}' )
        
        pyautogui.click( cursor )
        pyautogui.hotkey('ctrl', 'a')
        
        # lower the case to make it type faster
        pyautogui.typewrite(code.lower())
        
        time.sleep(len(code)*0.05)
        pyautogui.press( 'enter' )
        
        # add additional time to prevent it run next line before the game was ready
        time.sleep( wait_time + len(code)*char_time )
        

# Run the loop in separate thread
loop_thread = threading.Thread( target=input_loop )
loop_thread.start()





# Create and start the keyboard listener
def on_press( key ):
    global exiting
    try:
        # Check if Tab was pressed
        if key == keyboard.Key.tab:
            print( 'Tab key pressed, stopping the script in few seconds.' )
            exiting = True
            
    except AttributeError:
        pass
    
    if exiting:
        return False
    
with keyboard.Listener( on_press=on_press ) as listener:
    listener.join()





# Wait for loop thread to finish
loop_thread.join()
