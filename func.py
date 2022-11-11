import datetime
import webbrowser

def create_conference(url):
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"))
    webbrowser.get(using='edge').open_new_tab(url)

def get_date_now():
    now = datetime.datetime.now()
    time_now = now.strftime("%Y-%m-%d")
    return time_now

def main():
    print(get_date_now())
    create_conference("https://us05web.zoom.us/j/78289857291?pwd=K2lVaHlDK0I2b3Bzdllxa2xEVXo4UT09")

if __name__ == "__main__":
    main()
    