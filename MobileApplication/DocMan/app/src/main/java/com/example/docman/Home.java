package com.example.docman;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.net.Uri;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;

import static android.Manifest.permission.RECORD_AUDIO;
import static android.Manifest.permission.WRITE_EXTERNAL_STORAGE;





import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.net.Uri;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import static android.Manifest.permission.RECORD_AUDIO;
import static android.Manifest.permission.WRITE_EXTERNAL_STORAGE;
import static android.view.View.*;

public class Home extends AppCompatActivity {

    private Button startbtn, stopbtn, playbtn, stopplay, share,precautrions,logout,result,about,health;
        private MediaRecorder mRecorder;
        private MediaPlayer mPlayer;
        private static final String LOG_TAG = "AudioRecording";
        private static String mFileName = null;
        public static final int REQUEST_AUDIO_PERMISSION_CODE = 1;
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_home);
            startbtn = (Button)findViewById(R.id.btnRecord);
            stopbtn = (Button)findViewById(R.id.btnStop);
            playbtn = (Button)findViewById(R.id.btnPlay);
            stopplay = (Button)findViewById(R.id.btnStopPlay);
            share = (Button) findViewById(R.id.share);
            precautrions=(Button)findViewById(R.id.precautions);

            result=(Button)findViewById(R.id.result);
            about=(Button)findViewById(R.id.about);
            health=(Button)findViewById(R.id.health);
            stopbtn.setEnabled(true);
            playbtn.setEnabled(true);
            stopplay.setEnabled(true);
            mFileName = Environment.getExternalStorageDirectory().getAbsolutePath();
            mFileName += "/AudioRecording.mp3";
            final File file = new File(mFileName);

            share.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:bunnyrb4@gmail.com"));
                    intent.putExtra(Intent.EXTRA_STREAM,Uri.fromFile(file));
                    startActivity(intent);
                }
            });

            startbtn.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {
                    if(CheckPermissions()) {
                        stopbtn.setEnabled(true);
                        startbtn.setEnabled(false);
                        playbtn.setEnabled(false);
                        stopplay.setEnabled(false);
                        mRecorder = new MediaRecorder();
                        mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                        mRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
                        mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);
                        mRecorder.setOutputFile(mFileName);
                        try {
                            mRecorder.prepare();
                        } catch (IOException e) {
                            Log.e(LOG_TAG, "prepare() failed");
                        }
                        mRecorder.start();
                        Toast.makeText(getApplicationContext(),
                                "Recording Started", Toast.LENGTH_LONG).show();
                    }
                    else
                    {
                        RequestPermissions();
                    }
                }
            });
            stopbtn.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {
                    stopbtn.setEnabled(true);
                    startbtn.setEnabled(true);
                    playbtn.setEnabled(true);
                    stopplay.setEnabled(true);
                    mRecorder.stop();
                    mRecorder.release();
                    mRecorder = null;
                    Toast.makeText(getApplicationContext(), "Recording Stopped", Toast.LENGTH_LONG).show();
                }
            });
            playbtn.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {
                    stopbtn.setEnabled(true);
                    startbtn.setEnabled(true);
                    playbtn.setEnabled(false);
                    stopplay.setEnabled(true);
                    mPlayer = new MediaPlayer();
                    try {
                        mPlayer.setDataSource(mFileName);
                        mPlayer.prepare();
                        mPlayer.start();
                        Toast.makeText(getApplicationContext(), "Recording Started Playing", Toast.LENGTH_LONG).show();
                    } catch (IOException e) {
                        Log.e(LOG_TAG, "prepare() failed");
                    }
                }
            });
            stopplay.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {
                    mPlayer.release();
                    mPlayer = null;
                    stopbtn.setEnabled(true);
                    startbtn.setEnabled(true);
                    playbtn.setEnabled(true);
                    stopplay.setEnabled(false);
                    Toast.makeText(getApplicationContext(),"Playing Audio Stopped", Toast.LENGTH_SHORT).show();
                }
            });

            health.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {

                    startActivity(new Intent(Home.this,Health.class));
                }
            });

            precautrions.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {

                    startActivity(new Intent(Home.this,Precautions.class));
                }
            });
            about.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {

                    startActivity(new Intent(Home.this,About.class));
                }
            });
            result.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {

                    startActivity(new Intent(Home.this,Result.class));
                }
            });





        }
        @Override
        public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
            switch (requestCode) {
                case REQUEST_AUDIO_PERMISSION_CODE:
                    if (grantResults.length> 0) {
                        boolean permissionToRecord = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                        boolean permissionToStore = grantResults[1] ==  PackageManager.PERMISSION_GRANTED;
                        if (permissionToRecord && permissionToStore) {
                            Toast.makeText(getApplicationContext(), "Permission Granted", Toast.LENGTH_LONG).show();
                        } else {
                            Toast.makeText(getApplicationContext(),"Permission Denied",Toast.LENGTH_LONG).show();
                        }
                    }
                    break;
            }
        }
        public boolean CheckPermissions() {
            int result = ContextCompat.checkSelfPermission(getApplicationContext(), WRITE_EXTERNAL_STORAGE);
            int result1 = ContextCompat.checkSelfPermission(getApplicationContext(), RECORD_AUDIO);
            return result == PackageManager.PERMISSION_GRANTED && result1 == PackageManager.PERMISSION_GRANTED;
        }
        private void RequestPermissions() {
            ActivityCompat.requestPermissions(Home.this,
                    new String[]{RECORD_AUDIO, WRITE_EXTERNAL_STORAGE}, REQUEST_AUDIO_PERMISSION_CODE);
        }


    }