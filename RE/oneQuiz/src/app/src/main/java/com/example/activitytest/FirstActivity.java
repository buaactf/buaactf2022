package com.example.activitytest;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.util.Base64;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;

public class FirstActivity extends AppCompatActivity {
    public static byte[] encrypt(byte[] key, byte[] input) throws GeneralSecurityException {
        @SuppressLint("GetInstance") Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        SecretKey keySpec = new SecretKeySpec(key, "AES");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        return cipher.doFinal(input);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //向加载布局函数setContentView传入一个布局的ID
        //项目中添加的任何资源都会在R文件中生成一个相应的资源id
        setContentView(R.layout.first_layout);
        Button v1 = (Button) findViewById(R.id.button_1);
        v1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //由于活动本身就是一个Context对象，因此这里直接传入FirstActivity.this即可
//                Toast.makeText(FirstActivity.this, "You Clicked Button 1.", Toast.LENGTH_SHORT).show();
//                finish();
//                Intent intent = new Intent(FirstActivity.this,SecondActivity.class);
//                System.out.print(SecondActivity.class);
//                startActivity(intent);
                String v2 = ((EditText) FirstActivity.this.findViewById(R.id.editTextTextPassword)).getText().toString();
                byte[] v3 = "f1rstQu1z-Sec0nd".getBytes(StandardCharsets.UTF_8);
//                Toast.makeText(FirstActivity.this, "You input " + v2, Toast.LENGTH_LONG).show();

                byte[] v4 = new byte[0];
                try {
                    v4 = encrypt(v3, v2.getBytes(StandardCharsets.UTF_8));
                } catch (GeneralSecurityException e) {
                    e.printStackTrace();
                }
                if (Base64.encodeToString(v4, 0).replace("\n", "").equals("bzxH2b3uy05VZFoCl4h8RQdtRq6Pp8aQyIlvPTwK+ts=")) {
                    Toast.makeText(FirstActivity.this, "🎉🎉🎉🎉🎉", Toast.LENGTH_LONG).show();
//                    Intent v5 = new Intent(FirstActivity.this, SecondActivity.class);
//                    startActivity(v5);
                    return;
                }

                Toast.makeText(FirstActivity.this, "别急", Toast.LENGTH_LONG).show();

//                Intent intent = new Intent(FirstActivity.this, MAZE.class);

            }

        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        //通过getMenuInflater()方法能够得到MenuInflater对象
        //再调用它的inflate()方法就可以给当前活动创建菜单了
        getMenuInflater().inflate(R.menu.main,menu);
        //inflate()第一个参数用于指定我们通过哪一个资源文件来创建菜单
        //这里当然传入R.menu.main
        //第二个参数用于指定我们的菜单项将添加到哪一个Menu对象当中，
        //这里直接使用onCreateOptionsMenu()方法中传入的menu参数
        return true;//返回true，表示允许创建的菜单显示出来，
        //如果返回了false，创建的菜单将无法显示。
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        switch (item.getItemId()) {
            case R.id.add_item:
                Toast.makeText(this, "😡", Toast.LENGTH_SHORT).show();
                break;
            case R.id.remove_item:
                Toast.makeText(this, "😡", Toast.LENGTH_SHORT).show();
                break;
            default:
        }
        return true;
   }
}