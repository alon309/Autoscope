import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraManager;
import android.os.Build;
import android.util.Log;
import android.widget.Toast;
import androidx.core.content.ContextCompat;

import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbManager;

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
                        context, 0, new Intent(ACTION_USB_PERMISSION), 
                        Build.VERSION.SDK_INT >= Build.VERSION_CODES.M 
                        ? PendingIntent.FLAG_IMMUTABLE : 0);

                if (!usbManager.hasPermission(device)) {
                    usbManager.requestPermission(device, permissionIntent);
                }

                checkForExternalCamera(context);
            }
        }
    }

    private void checkForExternalCamera(Context context) {
        CameraManager manager = (CameraManager) context.getSystemService(Context.CAMERA_SERVICE);
        try {
            for (String cameraId : manager.getCameraIdList()) {
                CameraCharacteristics characteristics = manager.getCameraCharacteristics(cameraId);
                Integer lensFacing = characteristics.get(CameraCharacteristics.LENS_FACING);

                if (lensFacing != null && lensFacing == CameraCharacteristics.LENS_FACING_EXTERNAL) {
                    Log.d("UsbBroadcastReceiver", "External camera found: " + cameraId);
                    Toast.makeText(context, "External Camera Detected", Toast.LENGTH_SHORT).show();
                }
            }
        } catch (CameraAccessException e) {
            Log.e("UsbBroadcastReceiver", "Error accessing camera: ", e);
        }
    }
}
