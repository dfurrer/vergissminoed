package com.example.dev.vergissminoed;

import android.app.ListActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.File;

import android.os.Environment;


public class ShowList extends ListActivity {
    ArrayAdapter<String> mAdapter;

    private String url1 = "http://vergissminoed.appspot.com/?customerid=";
    private String userId = "156290";
    private HandleJSON obj;
    private String filename = "data_vergiss2";
    private ArrayList<Pair<Date, ArrayList<String>>> data;

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_list);
        try {
            // restore data
            //check whether data is available
            restore();
            if (data == null) {
                refresh();
            }

            DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
            Date d = dateFormat.parse("2014-10-10");

            //find todays list
            Pair<Date, ArrayList<String>> items = data.get(0);
            for (int i = 0; i < data.size() && !data.get(i).first.equals(d); i++) {
                items = data.get(i);
            }
            //ArrayList<String> items  = new ArrayList<String>(
            //       Arrays.asList("Milk", "Toilet paper", "Yoghurt", "Nespresso"));


            mAdapter = new ArrayAdapter<String>(this,
                    android.R.layout.simple_list_item_1,
                    android.R.id.text1,
                    items.second);
            setListAdapter(mAdapter);

            ListView listView = getListView();
            // Create a ListView-specific touch listener. ListViews are given special treatment because
            // by default they handle touches for their list items... i.e. they're in charge of drawing
            // the pressed state (the list selector), handling list item clicks, etc.
            SwipeDismissListViewTouchListener touchListener =
                    new SwipeDismissListViewTouchListener(
                            listView,
                            new SwipeDismissListViewTouchListener.DismissCallbacks() {
                                @Override
                                public boolean canDismiss(int position) {
                                    return true;
                                }

                                @Override
                                public void onDismiss(ListView listView, int[] reverseSortedPositions) {
                                    for (int position : reverseSortedPositions) {
                                        mAdapter.remove(mAdapter.getItem(position));
                                    }
                                    mAdapter.notifyDataSetChanged();
                                    store();
                                }
                            });
            listView.setOnTouchListener(touchListener);
            // Setting this scroll listener is required to ensure that during ListView scrolling,
            // we don't look for swipes.
            listView.setOnScrollListener(touchListener.makeScrollListener());
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    @Override
    protected void onListItemClick(ListView listView, View view, int position, long id) {
        Toast.makeText(this,
                "Clicked " + getListAdapter().getItem(position).toString(),
                Toast.LENGTH_SHORT).show();
    }

    private void refresh() {
        obj = new HandleJSON(url1 + userId);
        obj.fetchJSON();
        while (obj.parsingComplete) ;
        //Date today = new Date();
        data = obj.getData();
        store();

    }

    private void store() {
        try {

            File path = Environment.getExternalStoragePublicDirectory(
                    Environment.DIRECTORY_MOVIES);

            ObjectOutputStream objOut = new ObjectOutputStream(new FileOutputStream(new File(path, "/" + filename)));
            objOut.writeObject(data);
            objOut.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void restore() {
        try {
            File path = Environment.getExternalStoragePublicDirectory(
                    Environment.DIRECTORY_MOVIES);

            ObjectInputStream objIn = new ObjectInputStream(new FileInputStream(new File(path, "/" + filename)));
            data = (ArrayList<Pair<Date, ArrayList<String>>>) objIn.readObject();
            objIn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}