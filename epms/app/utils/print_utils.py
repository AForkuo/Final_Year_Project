import sys
import os

def print_file(filename, printer_name=None):
    if sys.platform.startswith('win'):
        # Windows-specific code
        import win32print
        import win32api
        
        if printer_name is None:
            printer_name = win32print.GetDefaultPrinter()
        
        try:
            win32api.ShellExecute(0, "print", filename, f'/d:"{printer_name}"', ".", 0)
            print(f"Print job sent to {printer_name}")
        except Exception as e:
            print(f"Failed to print: {e}")
    
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # Unix-based systems (Linux and macOS)
        import cups
        
        try:
            conn = cups.Connection()
            if printer_name is None:
                printer_name = conn.getDefault()
                if printer_name is None:
                    print("No default printer found.")
                    return
            
            job_id = conn.printFile(printer_name, filename, "Python Print Job", {})
            print(f"Print job sent to {printer_name}. Job ID: {job_id}")
        except cups.IPPError as e:
            print(f"Failed to print: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    else:
        print(f"Unsupported operating system: {sys.platform}")
