package com.example.jungle;

import android.os.Bundle;
import android.util.Log;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Build;
import java.net.NetworkInterface;
import java.util.Collections;
import java.util.List;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

class JungleWebViewClient extends WebViewClient {
    private static final String TAG = "JungleWebViewClient";
    private MainActivity activity;

    public JungleWebViewClient(MainActivity activity) {
        this.activity = activity;
    }

    @Override
    public void onPageFinished(WebView view, String url) {
        super.onPageFinished(view, url);
        Log.d(TAG, "WebView finished loading: " + url);
    }

    @Override
    public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
        super.onReceivedError(view, request, error);
        String errorMsg = "Error connecting to Flask server. Please try restarting the app.";
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
            Log.e(TAG, errorMsg + " - " + error.getDescription());
        } else {
            Log.e(TAG, errorMsg);
        }
        activity.showToast(errorMsg);
    }

    @Override
    public void onReceivedHttpError(WebView view, WebResourceRequest request, WebResourceResponse errorResponse) {
        super.onReceivedHttpError(view, request, errorResponse);
        Log.e(TAG, "HTTP Error: " + errorResponse.getStatusCode() + " " + errorResponse.getReasonPhrase());
    }
}

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private static final String TAG = "MainActivity";
    private static final int SERVER_PORT = 5000;
    private static final int SERVER_STARTUP_DELAY = 5000;
    private boolean isFlaskServerRunning = false;
    private Thread serverThread;
    private String serverUrl;

    private String getLocalIpAddress() {
        try {
            List<NetworkInterface> interfaces = Collections.list(NetworkInterface.getNetworkInterfaces());
            for (NetworkInterface intf : interfaces) {
                List<java.net.InetAddress> addrs = Collections.list(intf.getInetAddresses());
                for (java.net.InetAddress addr : addrs) {
                    if (!addr.isLoopbackAddress() && addr.getHostAddress().indexOf(':') == -1) {
                        String sAddr = addr.getHostAddress();
                        if (sAddr.startsWith("192.168.") || sAddr.startsWith("10.") || sAddr.startsWith("172.")) {
                            Log.d(TAG, "Found local IP: " + sAddr);
                            return sAddr;
                        }
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error getting IP address: " + e.getMessage());
        }
        return "127.0.0.1"; // Fallback to localhost if no other IP found
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getSupportActionBar() != null) {
            getSupportActionBar().hide();
        }
        setContentView(R.layout.activity_main);

        // Get local IP and set server URL
        String localIp = getLocalIpAddress();
        serverUrl = "http://" + localIp + ":" + SERVER_PORT;
        Log.d(TAG, "Server URL: " + serverUrl);

        Log.d(TAG, "Starting MainActivity...");

        // Initialize Python
        try {
            if (!Python.isStarted()) {
                Log.d(TAG, "Initializing Python...");
                Python.start(new AndroidPlatform(this));
                Log.d(TAG, "Python initialized successfully");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error initializing Python: " + e.getMessage(), e);
            showToast("Error initializing Python: " + e.getMessage());
            return;
        }

        // Set up WebView
        webView = findViewById(R.id.webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setAllowFileAccess(true);
        webView.getSettings().setAllowContentAccess(true);
        webView.setWebViewClient(new JungleWebViewClient(this));

        // Enable WebView debugging
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            WebView.setWebContentsDebuggingEnabled(true);
        }

        startFlaskServer();
    }

    private void startFlaskServer() {
        // Start Flask server in a background thread
        serverThread = new Thread(() -> {
            try {
                Log.d(TAG, "Getting Python instance...");
                Python py = Python.getInstance();
                
                Log.d(TAG, "Loading Flask server module...");
                PyObject serverModule = py.getModule("run_server");
                
                Log.d(TAG, "Starting Flask server...");
                isFlaskServerRunning = true;
                // Pass the local IP to Flask
                serverModule.callAttr("run_server", "0.0.0.0");
            } catch (Exception e) {
                isFlaskServerRunning = false;
                String errorMsg = "Error starting Flask server: " + e.getMessage();
                Log.e(TAG, errorMsg, e);
                runOnUiThread(() -> {
                    showToast(errorMsg);
                    String errorHtml = "<html><body style='padding: 20px;'>"
                        + "<h2>Error Starting Server</h2>"
                        + "<p>" + errorMsg + "</p>"
                        + "<pre>" + Log.getStackTraceString(e) + "</pre>"
                        + "</body></html>";
                    webView.loadData(errorHtml, "text/html", "UTF-8");
                });
            }
        });
        serverThread.start();

        // Wait for server to start and load URL in a separate thread
        new Thread(() -> {
            try {
                Log.d(TAG, "Waiting for server to start...");
                Thread.sleep(SERVER_STARTUP_DELAY);
                
                if (isFlaskServerRunning) {
                    Log.d(TAG, "Loading WebView URL: " + serverUrl);
                    runOnUiThread(() -> {
                        webView.loadUrl(serverUrl);
                        Log.d(TAG, "WebView URL loaded: " + serverUrl);
                    });
                } else {
                    Log.e(TAG, "Flask server failed to start");
                    runOnUiThread(() -> showToast("Flask server failed to start. Please restart the app."));
                }
            } catch (InterruptedException e) {
                Log.e(TAG, "Error while waiting: " + e.getMessage(), e);
            }
        }).start();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (serverThread != null && serverThread.isAlive()) {
            serverThread.interrupt();
        }
    }

    public void showToast(String message) {
        runOnUiThread(() -> Toast.makeText(this, message, Toast.LENGTH_LONG).show());
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
} 