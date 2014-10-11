package com.vergissminoed.dev.vergissminoed;

import java.io.Serializable;
/**
 * Created by uelipeter on 10/11/14.
 */
public class Pair<T extends Serializable, G extends Serializable > implements Serializable {
    public T first;
    public G second;

    public Pair(T f, G s){
        first = f;
        second = s;
    }

}
