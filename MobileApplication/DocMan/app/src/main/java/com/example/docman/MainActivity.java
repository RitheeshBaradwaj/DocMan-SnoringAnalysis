package com.example.docman;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;


import android.annotation.SuppressLint;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.FirebaseApp;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class MainActivity extends AppCompatActivity {

    private EditText userid;
    private EditText password;
    private Button login;
    private TextView reset,Registrationuser;
    private FirebaseAuth firebaseAuth;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        FirebaseApp.initializeApp(this);
        setContentView(R.layout.activity_main);
        userid = (EditText) findViewById(R.id.userid);
        password = (EditText) findViewById(R.id.userpass);
        login = (Button) findViewById(R.id.log);
        Registrationuser = (TextView) findViewById(R.id.toRegister);
        firebaseAuth = FirebaseAuth.getInstance();
        reset = (TextView)findViewById(R.id.resetPass);



        FirebaseUser user = firebaseAuth.getCurrentUser();

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                validate(userid.getText().toString(), password.getText().toString());
            }

        });


        Registrationuser.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                userid.setText("");
                password.setText("");
                startActivity(new Intent(MainActivity.this, Registration.class));
            }
        });

        reset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this,forgotpass.class));
            }
        });
    }

    private void validate(String user_name, String pass) {
        firebaseAuth.signInWithEmailAndPassword(user_name, pass).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
            @SuppressLint("ShowToast")
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                if (task.isSuccessful()) {
                    finish();

                    checkEmailverification();
                    Intent intent= new Intent(MainActivity.this,Home.class);
                    startActivity(intent);

                } else {
                    Toast.makeText(MainActivity.this, "INVALID CREDENTIALS", Toast.LENGTH_LONG).show();
                }
            }
        });

    }

    private void checkEmailverification()
    {
        FirebaseUser firebaseUser = firebaseAuth.getInstance().getCurrentUser();
        Boolean emailflag = firebaseUser.isEmailVerified();
        if (emailflag) {
            finish();
            startActivity(new Intent(MainActivity.this,Home.class));
        } else {
            Toast.makeText(this, "please verify your email address", Toast.LENGTH_SHORT);
            firebaseAuth.signOut();
        }




    }



}
