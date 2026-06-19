package com.rawjoy.app.bridge;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.webkit.JavascriptInterface;
import com.rawjoy.app.database.DatabaseHelper;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.UUID;

public class WebBridge {

    private final DatabaseHelper dbHelper;

    public WebBridge(Context context) {
        this.dbHelper = new DatabaseHelper(context);
    }

    @JavascriptInterface
    public String getCartItems() {
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        JSONArray jsonArray = new JSONArray();
        Cursor cursor = db.query(DatabaseHelper.TABLE_CART, null, null, null, null, null, null);

        try {
            while (cursor.moveToNext()) {
                JSONObject obj = new JSONObject();
                obj.put("productId", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_PROD_ID)));
                obj.put("name", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_NAME)));
                obj.put("variant", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_VAR_NAME)));
                obj.put("price", cursor.getDouble(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_PRICE)));
                obj.put("image", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_IMAGE)));
                obj.put("quantity", cursor.getInt(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_QTY)));
                jsonArray.put(obj);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            cursor.close();
        }

        return jsonArray.toString();
    }

    @JavascriptInterface
    public String addToCart(String productId, String name, String variant, double price, String imgUrl, int qty) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        JSONObject result = new JSONObject();

        try {
            // Check if item already exists
            Cursor cursor = db.query(DatabaseHelper.TABLE_CART, 
                    new String[]{DatabaseHelper.KEY_ID, DatabaseHelper.COL_CART_QTY},
                    DatabaseHelper.COL_CART_PROD_ID + "=? AND " + DatabaseHelper.COL_CART_VAR_NAME + "=?",
                    new String[]{productId, variant}, null, null, null);

            if (cursor.moveToFirst()) {
                // Update quantity
                int id = cursor.getInt(cursor.getColumnIndexOrThrow(DatabaseHelper.KEY_ID));
                int currentQty = cursor.getInt(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_QTY));
                ContentValues values = new ContentValues();
                values.put(DatabaseHelper.COL_CART_QTY, currentQty + qty);
                db.update(DatabaseHelper.TABLE_CART, values, DatabaseHelper.KEY_ID + "=?", new String[]{String.valueOf(id)});
            } else {
                // Insert new
                ContentValues values = new ContentValues();
                values.put(DatabaseHelper.COL_CART_PROD_ID, productId);
                values.put(DatabaseHelper.COL_CART_NAME, name);
                values.put(DatabaseHelper.COL_CART_VAR_NAME, variant);
                values.put(DatabaseHelper.COL_CART_PRICE, price);
                values.put(DatabaseHelper.COL_CART_IMAGE, imgUrl);
                values.put(DatabaseHelper.COL_CART_QTY, qty);
                db.insert(DatabaseHelper.TABLE_CART, null, values);
            }
            cursor.close();

            // Return success and total item count
            result.put("success", true);
            result.put("itemCount", getCartTotalCount(db));
        } catch (Exception e) {
            try {
                result.put("success", false);
                result.put("error", e.getMessage());
            } catch (Exception ignored) {}
        }

        return result.toString();
    }

    @JavascriptInterface
    public String updateCartItem(String productId, String variant, int qty) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        JSONObject result = new JSONObject();

        try {
            if (qty <= 0) {
                db.delete(DatabaseHelper.TABLE_CART, 
                        DatabaseHelper.COL_CART_PROD_ID + "=? AND " + DatabaseHelper.COL_CART_VAR_NAME + "=?",
                        new String[]{productId, variant});
            } else {
                ContentValues values = new ContentValues();
                values.put(DatabaseHelper.COL_CART_QTY, qty);
                db.update(DatabaseHelper.TABLE_CART, values,
                        DatabaseHelper.COL_CART_PROD_ID + "=? AND " + DatabaseHelper.COL_CART_VAR_NAME + "=?",
                        new String[]{productId, variant});
            }
            result.put("success", true);
        } catch (Exception e) {
            try {
                result.put("success", false);
                result.put("error", e.getMessage());
            } catch (Exception ignored) {}
        }

        return result.toString();
    }

    @JavascriptInterface
    public void clearCart() {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        db.delete(DatabaseHelper.TABLE_CART, null, null);
    }

    @JavascriptInterface
    public String createOrder(String orderJsonStr) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        JSONObject result = new JSONObject();
        db.beginTransaction();

        try {
            JSONObject orderJson = new JSONObject(orderJsonStr);
            String localId = "local_" + UUID.randomUUID().toString().substring(0, 8);
            
            ContentValues orderValues = new ContentValues();
            orderValues.put(DatabaseHelper.KEY_ID, localId);
            orderValues.put(DatabaseHelper.COL_ORD_TOTAL, orderJson.getDouble("total"));
            orderValues.put(DatabaseHelper.COL_ORD_STATUS, "pending");
            orderValues.put(DatabaseHelper.COL_ORD_SYNC, orderJson.optInt("synced", 0));
            orderValues.put(DatabaseHelper.COL_ORD_NOTES, orderJson.optString("notes", ""));
            orderValues.put(DatabaseHelper.COL_ORD_DATE, new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", java.util.Locale.US).format(new java.util.Date()));

            // Split shippingAddress fields
            String address = orderJson.getString("shippingAddress");
            String[] parts = address.split(",", 3);
            if (parts.length >= 3) {
                orderValues.put(DatabaseHelper.COL_ORD_NAME, parts[0].trim());
                orderValues.put(DatabaseHelper.COL_ORD_PHONE, parts[1].trim());
                orderValues.put(DatabaseHelper.COL_ORD_ADDRESS, parts[2].trim());
            } else {
                orderValues.put(DatabaseHelper.COL_ORD_ADDRESS, address);
            }

            db.insert(DatabaseHelper.TABLE_ORDERS, null, orderValues);

            // Insert items
            JSONArray items = orderJson.getJSONArray("items");
            for (int i = 0; i < items.length(); i++) {
                JSONObject item = items.getJSONObject(i);
                ContentValues itemValues = new ContentValues();
                itemValues.put("order_id", localId);
                itemValues.put(DatabaseHelper.COL_CART_PROD_ID, item.getString("productId"));
                itemValues.put(DatabaseHelper.COL_CART_VAR_NAME, item.optString("variant", ""));
                itemValues.put(DatabaseHelper.COL_CART_QTY, item.getInt("quantity"));
                itemValues.put(DatabaseHelper.COL_CART_PRICE, item.getDouble("price"));
                db.insert(DatabaseHelper.TABLE_ORDER_ITEMS, null, itemValues);
            }

            // Clear local cart
            db.delete(DatabaseHelper.TABLE_CART, null, null);

            db.setTransactionSuccessful();
            result.put("success", true);
            result.put("orderId", localId);
        } catch (Exception e) {
            e.printStackTrace();
            try {
                result.put("success", false);
                result.put("error", e.getMessage());
            } catch (Exception ignored) {}
        } finally {
            db.endTransaction();
        }

        return result.toString();
    }

    @JavascriptInterface
    public String getUserOrders() {
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        JSONArray jsonArray = new JSONArray();
        Cursor cursor = db.query(DatabaseHelper.TABLE_ORDERS, null, null, null, null, null, DatabaseHelper.COL_ORD_DATE + " DESC");

        try {
            while (cursor.moveToNext()) {
                JSONObject obj = new JSONObject();
                String orderId = cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.KEY_ID));
                obj.put("id", orderId);
                obj.put("total", cursor.getDouble(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_TOTAL)));
                obj.put("status", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_STATUS)));
                obj.put("synced", cursor.getInt(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_SYNC)));
                obj.put("createdAt", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_DATE)));
                obj.put("notes", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_NOTES)));
                
                String shippingAddress = cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_NAME)) + ", " +
                                         cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_PHONE)) + ", " +
                                         cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_ADDRESS));
                obj.put("shippingAddress", shippingAddress);

                // Fetch items for this order
                JSONArray itemsArray = new JSONArray();
                Cursor itemCursor = db.query(DatabaseHelper.TABLE_ORDER_ITEMS, null, 
                        "order_id=?", new String[]{orderId}, null, null, null);
                while (itemCursor.moveToNext()) {
                    JSONObject itemObj = new JSONObject();
                    itemObj.put("productId", itemCursor.getString(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_PROD_ID)));
                    itemObj.put("variant", itemCursor.getString(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_VAR_NAME)));
                    itemObj.put("quantity", itemCursor.getInt(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_QTY)));
                    itemObj.put("price", itemCursor.getDouble(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_PRICE)));
                    
                    // Fetch product name & image for details
                    Cursor prodCursor = db.query(DatabaseHelper.TABLE_PRODUCTS, 
                            new String[]{DatabaseHelper.COL_PROD_NAME, DatabaseHelper.COL_PROD_IMAGE},
                            DatabaseHelper.KEY_ID + "=?", 
                            new String[]{itemCursor.getString(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_PROD_ID))}, 
                            null, null, null);
                    if (prodCursor.moveToFirst()) {
                        itemObj.put("name", prodCursor.getString(prodCursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_NAME)));
                    } else {
                        itemObj.put("name", "RawFood Product");
                    }
                    prodCursor.close();
                    
                    itemsArray.put(itemObj);
                }
                itemCursor.close();
                obj.put("items", itemsArray);

                jsonArray.put(obj);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            cursor.close();
        }

        return jsonArray.toString();
    }

    @JavascriptInterface
    public String getUnsyncedOrders() {
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        JSONArray jsonArray = new JSONArray();
        Cursor cursor = db.query(DatabaseHelper.TABLE_ORDERS, null, 
                DatabaseHelper.COL_ORD_SYNC + "=0", null, null, null, null);

        try {
            while (cursor.moveToNext()) {
                JSONObject obj = new JSONObject();
                String orderId = cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.KEY_ID));
                obj.put("id", orderId);
                obj.put("total", cursor.getDouble(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_TOTAL)));
                obj.put("notes", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_NOTES)));
                
                String shippingAddress = cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_NAME)) + ", " +
                                         cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_PHONE)) + ", " +
                                         cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_ORD_ADDRESS));
                obj.put("shippingAddress", shippingAddress);

                JSONArray itemsArray = new JSONArray();
                Cursor itemCursor = db.query(DatabaseHelper.TABLE_ORDER_ITEMS, null, 
                        "order_id=?", new String[]{orderId}, null, null, null);
                while (itemCursor.moveToNext()) {
                    JSONObject itemObj = new JSONObject();
                    itemObj.put("productId", itemCursor.getString(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_PROD_ID)));
                    itemObj.put("variant", itemCursor.getString(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_VAR_NAME)));
                    itemObj.put("quantity", itemCursor.getInt(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_QTY)));
                    itemObj.put("price", itemCursor.getDouble(itemCursor.getColumnIndexOrThrow(DatabaseHelper.COL_CART_PRICE)));
                    itemsArray.put(itemObj);
                }
                itemCursor.close();
                obj.put("items", itemsArray);
                jsonArray.put(obj);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            cursor.close();
        }
        return jsonArray.toString();
    }

    @JavascriptInterface
    public void markOrderSynced(String localId, String remoteId) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.KEY_ID, remoteId);
        values.put(DatabaseHelper.COL_ORD_SYNC, 1);
        db.update(DatabaseHelper.TABLE_ORDERS, values, DatabaseHelper.KEY_ID + "=?", new String[]{localId});
    }

    @JavascriptInterface
    public String getProducts(String optionsJsonStr) {
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        JSONArray jsonArray = new JSONArray();

        String category = null;
        int limit = -1;
        try {
            if (optionsJsonStr != null && !optionsJsonStr.isEmpty() && !optionsJsonStr.equals("{}")) {
                JSONObject options = new JSONObject(optionsJsonStr);
                if (options.has("category")) {
                    category = options.getString("category");
                }
                if (options.has("limit")) {
                    limit = options.getInt("limit");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        String selection = null;
        String[] selectionArgs = null;
        if (category != null && !category.isEmpty()) {
            selection = DatabaseHelper.COL_PROD_CAT + " LIKE ?";
            selectionArgs = new String[]{category};
        }

        String limitStr = limit > 0 ? String.valueOf(limit) : null;

        Cursor cursor = db.query(DatabaseHelper.TABLE_PRODUCTS, null, selection, selectionArgs, null, null, null, limitStr);

        try {
            while (cursor.moveToNext()) {
                JSONObject prod = new JSONObject();
                String id = cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.KEY_ID));
                prod.put("id", id);
                prod.put("name", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_NAME)));
                prod.put("slug", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_SLUG)));
                prod.put("description", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_DESC)));
                prod.put("price", cursor.getDouble(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_PRICE)));
                prod.put("mainImage", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_IMAGE)));
                prod.put("category", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_CAT)));

                // Fetch variants for this product
                JSONArray varArray = new JSONArray();
                Cursor varCursor = db.query(DatabaseHelper.TABLE_VARIANTS, null,
                        DatabaseHelper.COL_VAR_PROD_ID + "=?", new String[]{id}, null, null, null);
                while (varCursor.moveToNext()) {
                    JSONObject var = new JSONObject();
                    var.put("name", varCursor.getString(varCursor.getColumnIndexOrThrow(DatabaseHelper.COL_VAR_SIZE)));
                    var.put("price", varCursor.getDouble(varCursor.getColumnIndexOrThrow(DatabaseHelper.COL_VAR_PRICE)));
                    varArray.put(var);
                }
                varCursor.close();
                prod.put("variants", varArray);

                jsonArray.put(prod);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            cursor.close();
        }

        return jsonArray.toString();
    }

    @JavascriptInterface
    public String getProductBySlug(String slug) {
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        JSONObject prod = null;

        Cursor cursor = db.query(DatabaseHelper.TABLE_PRODUCTS, null,
                DatabaseHelper.COL_PROD_SLUG + "=?", new String[]{slug}, null, null, null);

        try {
            if (cursor.moveToFirst()) {
                prod = new JSONObject();
                String id = cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.KEY_ID));
                prod.put("id", id);
                prod.put("name", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_NAME)));
                prod.put("slug", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_SLUG)));
                prod.put("description", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_DESC)));
                prod.put("price", cursor.getDouble(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_PRICE)));
                prod.put("mainImage", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_IMAGE)));
                prod.put("category", cursor.getString(cursor.getColumnIndexOrThrow(DatabaseHelper.COL_PROD_CAT)));

                // Fetch variants for this product
                JSONArray varArray = new JSONArray();
                Cursor varCursor = db.query(DatabaseHelper.TABLE_VARIANTS, null,
                        DatabaseHelper.COL_VAR_PROD_ID + "=?", new String[]{id}, null, null, null);
                while (varCursor.moveToNext()) {
                    JSONObject var = new JSONObject();
                    var.put("name", varCursor.getString(varCursor.getColumnIndexOrThrow(DatabaseHelper.COL_VAR_SIZE)));
                    var.put("price", varCursor.getDouble(varCursor.getColumnIndexOrThrow(DatabaseHelper.COL_VAR_PRICE)));
                    varArray.put(var);
                }
                varCursor.close();
                prod.put("variants", varArray);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            cursor.close();
        }

        return prod != null ? prod.toString() : null;
    }

    private int getCartTotalCount(SQLiteDatabase db) {
        Cursor cursor = db.rawQuery("SELECT SUM(" + DatabaseHelper.COL_CART_QTY + ") FROM " + DatabaseHelper.TABLE_CART, null);
        int total = 0;
        if (cursor.moveToFirst()) {
            total = cursor.getInt(0);
        }
        cursor.close();
        return total;
    }
}
