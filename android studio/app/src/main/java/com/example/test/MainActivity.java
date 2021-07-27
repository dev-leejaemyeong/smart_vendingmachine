package com.example.test;

import android.app.DatePickerDialog;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;


public class MainActivity extends AppCompatActivity {
    String host = "220.69.249.219";
    int port = 8100;
    static String temp="";
    LinearLayout dl,al,ml,tl;
    TextView dname1,dname2,dname3,dremains1,dremains2,dremains3,dsales1,dsales2,dsales3
   ,aname1,aname2,aname3,asales1,asales2,asales3,asalesprice1,asalesprice2,asalesprice3
   ,mname1,mname2,mname3,msales1,msales2,msales3,msalesprice1,msalesprice2,msalesprice3
   ,tname1,tname2,tname3,tsales1,tsales2,tsales3,tsalesprice1,tsalesprice2,tsalesprice3;
    DHandler dhandler= new DHandler();
    AHandler ahandler= new AHandler();
    THandler thandler= new THandler();
    MHandler mhandler= new MHandler();
    Button btn3;
    LinearLayout layout;
    DatePickerDialog.OnDateSetListener d = new DatePickerDialog.OnDateSetListener() {
        @Override
        public void onDateSet(DatePicker view, int year, int monthOfYear, int dayOfMonth) {

            client c=new client("m0"+monthOfYear);
            c.start();
            Log.d("YearMonthPickerTest", "year = " + year + ", month = " + monthOfYear + ", day = " + dayOfMonth);
        }
    };
    class client extends Thread{
        String command="";
        public client(String p){
            command=p;
        }
        @Override
        public void run() {
            try {
                Socket socket = new Socket(host, port);
                DataOutputStream outstream = new DataOutputStream(socket.getOutputStream());
                InputStream receiver = socket.getInputStream();
                outstream.writeUTF(command);
                outstream.flush();
                Log.d("ClientStream", "Sent to server.");
                InputStreamReader i=new InputStreamReader(socket.getInputStream());
                char letter;
                while (true){
                    letter=(char)i.read();
                    temp+=letter;
                    if (letter=='^'){
                        break;
                    }
                }
                Log.d("ClientThread","받은 데이터 : "+temp);
                Message message;
                Bundle bundle;
                switch (this.command){
                    case "d":
                        message = dhandler.obtainMessage();
                        bundle = new Bundle();
                        bundle.putString("value", temp);
                        message.setData(bundle);
                        //sendMessage가 되면 이 handler가 해당되는 핸들러객체가(ValueHandler) 자동으로 호출된다.
                        dhandler.sendMessage(message);
                        break;

                    case "a":
                        message = ahandler.obtainMessage();
                        bundle = new Bundle();
                        bundle.putString("value", temp);
                        message.setData(bundle);
                        //sendMessage가 되면 이 handler가 해당되는 핸들러객체가(ValueHandler) 자동으로 호출된다.
                        ahandler.sendMessage(message);
                        break;
                    case "t":
                        message = thandler.obtainMessage();
                        bundle = new Bundle();
                        bundle.putString("value", temp);
                        message.setData(bundle);
                        //sendMessage가 되면 이 handler가 해당되는 핸들러객체가(ValueHandler) 자동으로 호출된다.
                        thandler.sendMessage(message);
                        break;
                    default:
                        message = mhandler.obtainMessage();
                        bundle = new Bundle();
                        bundle.putString("value", temp);
                        message.setData(bundle);
                        //sendMessage가 되면 이 handler가 해당되는 핸들러객체가(ValueHandler) 자동으로 호출된다.
                        mhandler.sendMessage(message);
                        break;

                }

                socket.close();

            } catch (Exception e) {
                e.printStackTrace();
            }
            finally {
                Log.d("ClientThread", "Received data:asd ");
            }
        }}

    class DHandler extends Handler{
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            Bundle bundle = msg.getData();
            //String value = bundle.getString("value");
            String result = temp.substring(0,temp.length()-1);
            String[] array = result.split("/");
            String[] arr1 = array[0].split(" ");
            String[] arr2 = array[1].split(" ");
            String[] arr3 = array[2].split(" ");
            dl.setVisibility(View.VISIBLE);
            al.setVisibility(View.INVISIBLE);
            ml.setVisibility(View.INVISIBLE);
            tl.setVisibility(View.INVISIBLE);
            dname1.setText(arr1[0]);
            dremains1.setText(arr1[1]);
            dsales1.setText(arr1[2]);

            dname2.setText(arr2[0]);
            dremains2.setText(arr2[1]);
            dsales2.setText(arr2[2]);

            dname3.setText(arr3[0]);
            dremains3.setText(arr3[1]);
            dsales3.setText(arr3[2]);
            temp="";
        }
    }
    class AHandler extends Handler{
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            Bundle bundle = msg.getData();
            //String value = bundle.getString("value");
            String result = temp.substring(0,temp.length()-1);
            String[] array = result.split(" ");
            dl.setVisibility(View.INVISIBLE);
            al.setVisibility(View.VISIBLE);
            ml.setVisibility(View.INVISIBLE);
            tl.setVisibility(View.INVISIBLE);


            aname1.setText("Coke");
            asales1.setText(array[0]);
            asalesprice1.setText(Integer.toString(Integer.parseInt(array[0])*300));
            aname2.setText("Pepsi");
            asales2.setText(array[1]);
            asalesprice2.setText(Integer.toString(Integer.parseInt(array[1])*300));
            aname3.setText("Sprite");
            asales3.setText(array[2]);
            asalesprice3.setText(Integer.toString(Integer.parseInt(array[2])*300));

            temp="";
        }
    }
    class MHandler extends Handler{
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            Bundle bundle = msg.getData();
            //String value = bundle.getString("value");
            String result = temp.substring(0,temp.length()-1);
            String[] array = result.split(" ");
            dl.setVisibility(View.INVISIBLE);
            al.setVisibility(View.INVISIBLE);
            ml.setVisibility(View.VISIBLE);
            tl.setVisibility(View.INVISIBLE);


            mname1.setText("Coke");
            msales1.setText(array[0]);
            msalesprice1.setText(Integer.toString(Integer.parseInt(array[0])*300));
            mname2.setText("Pepsi");
            msales2.setText(array[1]);
            msalesprice2.setText(Integer.toString(Integer.parseInt(array[2])*300));
            mname3.setText("Sprite");
            msales3.setText(array[2]);
            msalesprice3.setText(Integer.toString(Integer.parseInt(array[2])*300));
            temp="";
        }
    }
    class THandler extends Handler{
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            Bundle bundle = msg.getData();
            //String value = bundle.getString("value");
            String result = temp.substring(0,temp.length()-1);
            String[] array = result.split(" ");
            dl.setVisibility(View.INVISIBLE);
            al.setVisibility(View.INVISIBLE);
            ml.setVisibility(View.INVISIBLE);
            tl.setVisibility(View.VISIBLE);


            tname1.setText("Coke");
            tsales1.setText(array[0]);
            tsalesprice1.setText(Integer.toString(Integer.parseInt(array[0])*300));
            tname2.setText("Pepsi");
            tsales2.setText(array[1]);
            tsalesprice2.setText(Integer.toString(Integer.parseInt(array[1])*300));
            tname3.setText("Sprite");
            tsales3.setText(array[2]);
            tsalesprice3.setText(Integer.toString(Integer.parseInt(array[2])*300));
            temp="";
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {




        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        dl=findViewById(R.id.dLayout);
        al=findViewById(R.id.aLayout);
        ml=findViewById(R.id.mLayout);
        tl=findViewById(R.id.tLayout);
        layout=findViewById(R.id.layout);
        layout.setBackgroundResource(R.drawable.back);
        dl.setVisibility(View.VISIBLE);
        al.setVisibility(View.INVISIBLE);
        ml.setVisibility(View.INVISIBLE);
        tl.setVisibility(View.INVISIBLE);
        dname1 = (TextView)findViewById(R.id.name1);
        dremains1 = (TextView)findViewById(R.id.remains1);
        dsales1 = (TextView)findViewById(R.id.sales1);
        dname2 = (TextView)findViewById(R.id.name2);
        dremains2 = (TextView)findViewById(R.id.remains2);
        dsales2 = (TextView)findViewById(R.id.sales2);
        dname3 = (TextView)findViewById(R.id.name3);
        dremains3 = (TextView)findViewById(R.id.remains3);
        dsales3 = (TextView)findViewById(R.id.sales3);
        aname1 = (TextView)findViewById(R.id.aname1);
        asalesprice1 = (TextView)findViewById(R.id.asalesprice1);
        asales1 = (TextView)findViewById(R.id.asales1);
        aname2 = (TextView)findViewById(R.id.aname2);
        asalesprice2 = (TextView)findViewById(R.id.asalesprice2);
        asales2 = (TextView)findViewById(R.id.asales2);
        aname3 = (TextView)findViewById(R.id.aname3);
        asalesprice3 = (TextView)findViewById(R.id.asalesprice3);
        asales3 = (TextView)findViewById(R.id.asales3);
        mname1 = (TextView)findViewById(R.id.mname1);
        msalesprice1 = (TextView)findViewById(R.id.msalesprice1);
        msales1 = (TextView)findViewById(R.id.msales1);
        mname2 = (TextView)findViewById(R.id.mname2);
        msalesprice2 = (TextView)findViewById(R.id.msalesprice2);
        msales2 = (TextView)findViewById(R.id.msales2);
        mname3 = (TextView)findViewById(R.id.mname3);
        msalesprice3 = (TextView)findViewById(R.id.msalesprice3);
        msales3 = (TextView)findViewById(R.id.msales3);
        tname1 = (TextView)findViewById(R.id.tname1);
        tsalesprice1 = (TextView)findViewById(R.id.tsalesprice1);
        tsales1 = (TextView)findViewById(R.id.tsales1);
        tname2 = (TextView)findViewById(R.id.tname2);
        tsalesprice2 = (TextView)findViewById(R.id.tsalesprice2);
        tsales2 = (TextView)findViewById(R.id.tsales2);
        tname3 = (TextView)findViewById(R.id.tname3);
        tsalesprice3 = (TextView)findViewById(R.id.tsalesprice3);
        tsales3 = (TextView)findViewById(R.id.tsales3);

        Button dbtn =findViewById(R.id.dbtn);
        Button abtn = findViewById(R.id.abtn);
        Button mbtn = findViewById(R.id.mbtn);
        Button tbtn = findViewById(R.id.tbtn);
        abtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                client c=new client("a");
                c.start();
            }
        });
        tbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                client c=new client("t");
                c.start();
            }
        });
        dbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                client c=new client("d");
                c.start();
            }
        });
        mbtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                test3 pd = new test3();
                pd.setListener(d);
                pd.show(getSupportFragmentManager(), "YearMonthPickerTest");

            }
        });

    }

}

