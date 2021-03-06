package com.vergissminoed.dev.vergissminoed;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.text.SimpleDateFormat;

import android.os.AsyncTask;

import org.json.JSONArray;
import org.json.JSONObject;

import android.annotation.SuppressLint;

public class HandleJSON {

    private ArrayList<Pair<Date, ArrayList<String>>> data;
    private String urlString = null;

    private ShowListActivity parentList;

    public HandleJSON(String url, ShowListActivity parent) {
        this.urlString = url;
        this.parentList = parent;
    }

    public ArrayList<Pair<Date, ArrayList<String>>> getData() {
        return data;
    }

    @SuppressLint("NewApi")
    public void readAndParseJSON(String in) {
        try {
            JSONObject reader = new JSONObject(in);
            DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");


            Iterator<String> it = reader.keys();

            data = new ArrayList<Pair<Date, ArrayList<String>>>(reader.length());

            for (int e = 0; it.hasNext(); e++) {
                String s = it.next();
                Date d = dateFormat.parse(s);
                ArrayList<String> strings = new ArrayList<String>();
                JSONArray jsonarray = reader.getJSONArray(s);
                for (int i = 0; i < jsonarray.length(); i++) {
                    strings.add(jsonarray.getString(i));
                }
                data.add(e, new Pair<Date, ArrayList<String>>(d, strings));

            }


        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    public void fetchJSON() {
        new AsyncTask<Void, Void, Void>() {
            @Override
            public Void doInBackground(Void... Params) {
                try {
                    URL url = new URL(urlString);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setReadTimeout(10000 /* milliseconds */);
                    conn.setConnectTimeout(15000 /* milliseconds */);
                    conn.setRequestMethod("GET");
                    conn.setDoInput(true);
                    // Starts the query
                    conn.connect();
                    InputStream stream = conn.getInputStream();

                    String da = convertStreamToString(stream);

                    readAndParseJSON(da);
                    stream.close();

                } catch (Exception e) {
                    e.printStackTrace();
                }
                return null;
            }

            @Override
            protected void onPostExecute(Void params) {
                parentList.refreshCallBack();
            }


        }.execute();
    }

    static String convertStreamToString(java.io.InputStream is) {
        java.util.Scanner s = new java.util.Scanner(is).useDelimiter("\\A");
        return s.hasNext() ? s.next() : "";
    }

}
