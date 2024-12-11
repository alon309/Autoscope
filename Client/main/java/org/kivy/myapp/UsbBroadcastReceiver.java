package org.kivy.myapp;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbManager;
import android.app.PendingIntent;

public class UsbBroadcastReceiver extends BroadcastReceiver {
    private static final String ACTION_USB_PERMISSION = "org.kivy.myapp.USB_PERMISSION";

    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        if (UsbManager.ACTION_USB_DEVICE_ATTACHED.equals(action)) {
            UsbDevice device = intent.getParcelableExtra(UsbManager.EXTRA_DEVICE);
            if (device != null) {
                UsbManager usbManager = (UsbManager) context.getSystemService(Context.USB_SERVICE);
                PendingIntent permissionIntent = PendingIntent.getBroadcast(
                        context, 0, new Intent(ACTION_USB_PERMISSION), PendingIntent.FLAG_MUTABLE);
                usbManager.requestPermission(device, permissionIntent);
                System.out.println("USB Device Attached: " + device.getDeviceName());
            }
        }
    }

}
