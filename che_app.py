from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast("Title", "This is a notification!",
                  icon_path="path/to/your/icon.png",
                  duration=5)  # Duration in seconds (optional)