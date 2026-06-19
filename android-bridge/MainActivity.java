package com.rawjoy.app;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;
import com.rawjoy.app.bridge.WebBridge;

public class MainActivity extends AppCompatActivity {
    private WebView mWebView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mWebView = findViewById(R.id.webview_rawjoy);
        WebSettings webSettings = mWebView.getSettings();
        
        // 1. Enable JavaScript execution
        webSettings.setJavaScriptEnabled(true);
        
        // 2. Wajib untuk LocalStorage (Firebase & local state)
        webSettings.setDomStorageEnabled(true); 
        
        // 3. Wajib untuk offline file access & ES Modules dari file://
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        webSettings.setAllowFileAccessFromFileURLs(true);
        webSettings.setAllowUniversalAccessFromFileURLs(true);
        
        // 4. Force links to open inside the app instead of launching system browser
        mWebView.setWebViewClient(new WebViewClient());
        
        // 5. Register Javascript interface bridge
        mWebView.addJavascriptInterface(new WebBridge(this), "AndroidDB");
        
        // 6. Load local assets
        mWebView.loadUrl("file:///android_asset/RawJoy/index.html");
    }
    
    // Handle physical back button to navigate backwards in web history
    @Override
    public void onBackPressed() {
        if (mWebView.canGoBack()) {
            mWebView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
