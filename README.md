# Show NordVPN status in Ubuntu indicator applet

## Dependencies
  - The official NordVPN client must be
  [installed](https://nordvpn.com/download/linux/").
  - Ubuntu packages: `sudo apt-get install -y gir1.2-appindicator python3-gi`

## Run
  - Login to NordVPN via the command line `nordvpn login`.
  - Once logged in, this app can be run as `python3 nordvpn_indicator.py`. You should see the
  status icon in your indicator applet (system tray).

Use [startup applications](https://help.ubuntu.com/stable/ubuntu-help/startup-applications.html.en)
to add this to your computer startup.

# A Better App
This indicator only shows the connection status. After I started writing this one, I found [another
app](https://github.com/yorickvanzweeden/Ubuntu-NordVPN-Indicator) with more complete features.
I ended up liking that one, so I made [my own fork](https://github.com/vaivaswatha/Ubuntu-NordVPN-Indicator)
of it, with the main difference being the icons and that the install script installs to
`$HOME`, and hence doesn't require root permissions.
