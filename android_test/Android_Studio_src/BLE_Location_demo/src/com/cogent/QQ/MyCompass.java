package com.cogent.QQ;

/**
 * Created by mayintong on 2015/8/6.
 */

import android.app.Activity;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

import java.util.List;

public class MyCompass extends Activity implements SensorEventListener
{
    //private CompassView    _compassView;
    private boolean        mRegisteredSensor;
    //����SensorManager
    private SensorManager mSensorManager;
    public float x;
    /** Called when the activity is first created. */
    public MyCompass(Context context) {
        mRegisteredSensor = false;
        //ȡ��SensorManagerʵ��
        mSensorManager = (SensorManager)context.getSystemService(Context.SENSOR_SERVICE);
        List<Sensor> sensors = mSensorManager.getSensorList(Sensor.TYPE_ORIENTATION);
        Sensor sensor = sensors.get(0);
        mSensorManager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_FASTEST);
    }



    @Override
    protected void onPause()
    {
        if (mRegisteredSensor)
        {
            //���������registerListener
            //����������ҪunregisterListener��ж��/ȡ��ע��
            mSensorManager.unregisterListener(this);
            mRegisteredSensor = false;
        }
        super.onPause();
    }
    //����׼�ȷ����ı�ʱ
    //sensor->������
    //accuracy->��׼��
    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy)
    {

    }
    // ���������ڱ��ı�ʱ����
    @Override
    public void onSensorChanged(SensorEvent event)
    {
        // ���ܷ����Ӧ��������
        if (event.sensor.getType() == Sensor.TYPE_ORIENTATION)
        {
            // �������ǿ��Եõ����ݣ�Ȼ�������Ҫ������
            x = event.values[SensorManager.DATA_X];

            //_compassView.setDegree(x);

        }
    }
}