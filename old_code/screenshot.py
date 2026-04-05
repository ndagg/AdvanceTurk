# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 17:53:24 2025

@author: ndagg
"""
import mss

import win32gui
import win32con
import win32com.client

import time
import numpy as np


class Screenshotter:
    
    def __init__(self):
        # Note, does hwnd change if other windows get opened/closed?
        self.hwnd = win32gui.FindWindow(None, "View Game - AWBW — Mozilla Firefox")
        
    def force_activate_window(self):
    
        # If minimized, restore the window
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
    
        # Use shell to bypass focus restrictions
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')  # Simulate ALT key to allow SetForegroundWindow
        win32gui.SetForegroundWindow(self.hwnd)
        # Ensure maximised
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWMAXIMIZED)
        
        # Block momentarily to give time to maximise
        time.sleep(0.5)
    
        return self.hwnd
    
    def take_screenshot(self, box=None, colour=False):
        
        self.force_activate_window()
               
        with mss.mss() as sct:
            # Get information of monitor 2
            monitor_number = 2
            mon = sct.monitors[monitor_number]
        
            # The screen part to capture
            if box is None:
                monitor = {
                    "top": mon["top"]+120,
                    "left": mon["left"]+30,
                    "width": mon["width"]-60,
                    "height": mon["height"]-170,
                    "mon": monitor_number,
                    }
            else:
                # Get window dimensions
                left, top, right, bottom = box[:4]
                width = right - left
                height = bottom - top
                monitor = {
                    "top":top+120,
                    "left": left+30,
                    "width": width-60,
                    "height": height-170,
                    "mon": monitor_number,
                    }
            img = np.array(sct.grab(monitor))[:,:,-2::-1]
        
        if not colour:
            img = np.sum(img, 2)//3
            img = img.astype("uint8")
        return img
    


