package com.rawjoy.app.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import org.json.JSONArray;
import org.json.JSONObject;

public class DatabaseHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "rawjoy.db";
    private static final int DATABASE_VERSION = 1;

    private final Context mContext;

    // Table names
    public static final String TABLE_PRODUCTS = "products";
    public static final String TABLE_VARIANTS = "variants";
    public static final String TABLE_CART = "cart_items";
    public static final String TABLE_ORDERS = "orders";
    public static final String TABLE_ORDER_ITEMS = "order_items";

    // Common column names
    public static final String KEY_ID = "id";

    // Products table columns
    public static final String COL_PROD_NAME = "name";
    public static final String COL_PROD_SLUG = "slug";
    public static final String COL_PROD_DESC = "description";
    public static final String COL_PROD_PRICE = "price";
    public static final String COL_PROD_IMAGE = "image_url";
    public static final String COL_PROD_CAT = "category";

    // Variants table columns
    public static final String COL_VAR_PROD_ID = "product_id";
    public static final String COL_VAR_SIZE = "size";
    public static final String COL_VAR_PRICE = "price";

    // Cart table columns
    public static final String COL_CART_PROD_ID = "product_id";
    public static final String COL_CART_VAR_NAME = "variant_name";
    public static final String COL_CART_QTY = "quantity";
    public static final String COL_CART_PRICE = "price";
    public static final String COL_CART_IMAGE = "image_url";
    public static final String COL_CART_NAME = "name";

    // Orders table columns
    public static final String COL_ORD_NAME = "customer_name";
    public static final String COL_ORD_EMAIL = "customer_email";
    public static final String COL_ORD_PHONE = "customer_phone";
    public static final String COL_ORD_TOTAL = "total_amount";
    public static final String COL_ORD_STATUS = "status";
    public static final String COL_ORD_SYNC = "synced"; // 0 for unsynced, 1 for synced
    public static final String COL_ORD_DATE = "created_at";
    public static final String COL_ORD_NOTES = "notes";
    public static final String COL_ORD_ADDRESS = "shipping_address";

    // Table Create Statements
    private static final String CREATE_TABLE_PRODUCTS = "CREATE TABLE " + TABLE_PRODUCTS + "("
            + KEY_ID + " TEXT PRIMARY KEY,"
            + COL_PROD_NAME + " TEXT NOT NULL,"
            + COL_PROD_SLUG + " TEXT UNIQUE,"
            + COL_PROD_DESC + " TEXT,"
            + COL_PROD_PRICE + " REAL,"
            + COL_PROD_IMAGE + " TEXT,"
            + COL_PROD_CAT + " TEXT" + ")";

    private static final String CREATE_TABLE_VARIANTS = "CREATE TABLE " + TABLE_VARIANTS + "("
            + KEY_ID + " INTEGER PRIMARY KEY AUTOINCREMENT,"
            + COL_VAR_PROD_ID + " TEXT,"
            + COL_VAR_SIZE + " TEXT,"
            + COL_VAR_PRICE + " REAL,"
            + "FOREIGN KEY(" + COL_VAR_PROD_ID + ") REFERENCES " + TABLE_PRODUCTS + "(" + KEY_ID + ")" + ")";

    private static final String CREATE_TABLE_CART = "CREATE TABLE " + TABLE_CART + "("
            + KEY_ID + " INTEGER PRIMARY KEY AUTOINCREMENT,"
            + COL_CART_PROD_ID + " TEXT NOT NULL,"
            + COL_CART_NAME + " TEXT,"
            + COL_CART_VAR_NAME + " TEXT,"
            + COL_CART_PRICE + " REAL,"
            + COL_CART_IMAGE + " TEXT,"
            + COL_CART_QTY + " INTEGER DEFAULT 1,"
            + "UNIQUE(" + COL_CART_PROD_ID + ", " + COL_CART_VAR_NAME + ")" + ")";

    private static final String CREATE_TABLE_ORDERS = "CREATE TABLE " + TABLE_ORDERS + "("
            + KEY_ID + " TEXT PRIMARY KEY,"
            + COL_ORD_NAME + " TEXT,"
            + COL_ORD_EMAIL + " TEXT,"
            + COL_ORD_PHONE + " TEXT,"
            + COL_ORD_ADDRESS + " TEXT,"
            + COL_ORD_TOTAL + " REAL,"
            + COL_ORD_STATUS + " TEXT DEFAULT 'pending',"
            + COL_ORD_SYNC + " INTEGER DEFAULT 0,"
            + COL_ORD_NOTES + " TEXT,"
            + COL_ORD_DATE + " TEXT" + ")";

    private static final String CREATE_TABLE_ORDER_ITEMS = "CREATE TABLE " + TABLE_ORDER_ITEMS + "("
            + KEY_ID + " INTEGER PRIMARY KEY AUTOINCREMENT,"
            + "order_id TEXT,"
            + COL_CART_PROD_ID + " TEXT,"
            + COL_CART_VAR_NAME + " TEXT,"
            + COL_CART_QTY + " INTEGER,"
            + COL_CART_PRICE + " REAL,"
            + "FOREIGN KEY(order_id) REFERENCES " + TABLE_ORDERS + "(" + KEY_ID + ")" + ")";

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        this.mContext = context;
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // creating required tables
        db.execSQL(CREATE_TABLE_PRODUCTS);
        db.execSQL(CREATE_TABLE_VARIANTS);
        db.execSQL(CREATE_TABLE_CART);
        db.execSQL(CREATE_TABLE_ORDERS);
        db.execSQL(CREATE_TABLE_ORDER_ITEMS);

        // Seed products from assets/RawJoy/firebase/seed-data.json
        seedDatabase(db);
    }

    private void seedDatabase(SQLiteDatabase db) {
        try {
            java.io.InputStream is = mContext.getAssets().open("RawJoy/firebase/seed-data.json");
            int size = is.available();
            byte[] buffer = new byte[size];
            is.read(buffer);
            is.close();
            String jsonStr = new String(buffer, "UTF-8");

            JSONObject root = new JSONObject(jsonStr);
            JSONArray products = root.getJSONArray("products");

            for (int i = 0; i < products.length(); i++) {
                JSONObject prod = products.getJSONObject(i);
                String id = prod.getString("id");
                String name = prod.getString("name");
                String slug = prod.getString("slug");
                String desc = prod.optString("description", "");
                double price = prod.optDouble("price", 0.0);
                String mainImage = prod.optString("mainImage", "");
                String category = prod.optString("category", "");

                ContentValues prodValues = new ContentValues();
                prodValues.put(KEY_ID, id);
                prodValues.put(COL_PROD_NAME, name);
                prodValues.put(COL_PROD_SLUG, slug);
                prodValues.put(COL_PROD_DESC, desc);
                prodValues.put(COL_PROD_PRICE, price);
                prodValues.put(COL_PROD_IMAGE, mainImage);
                prodValues.put(COL_PROD_CAT, category);

                db.insert(TABLE_PRODUCTS, null, prodValues);

                // Seed variants
                if (prod.has("variants")) {
                    JSONArray variants = prod.getJSONArray("variants");
                    for (int j = 0; j < variants.length(); j++) {
                        JSONObject variant = variants.getJSONObject(j);
                        String varName = variant.getString("name");
                        double varPrice = variant.getDouble("price");

                        ContentValues varValues = new ContentValues();
                        varValues.put(COL_VAR_PROD_ID, id);
                        varValues.put(COL_VAR_SIZE, varName);
                        varValues.put(COL_VAR_PRICE, varPrice);

                        db.insert(TABLE_VARIANTS, null, varValues);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // on upgrade drop older tables
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_PRODUCTS);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_VARIANTS);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_CART);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_ORDERS);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_ORDER_ITEMS);

        // create new tables
        onCreate(db);
    }
}
