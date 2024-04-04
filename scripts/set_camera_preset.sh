#!/bin/sh
# modprobe -rf uvcvideo
# modprobe uvcvideo nodrop=1 timeout=5000 quirks=0x80
v4l2-ctl -c white_balance_automatic=0,white_balance_temperature=7700,gain=255,auto_exposure=1,exposure_time_absolute=34,exposure_dynamic_framerate=0,focus_automatic_continuous=0;
v4l2-ctl -c focus_absolute=70;