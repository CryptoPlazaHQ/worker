# Streamlit_app
(.venv) PS C:\Users\DELL\Desktop\dashboards> streamlit run streamlit_app/app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.4:8501

  Stopping...
(.venv) PS C:\Users\DELL\Desktop\dashboards> streamlit run streamlit_app/app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.4:8501

2025-12-09 06:38:23,412 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/fiat_currencies with params: None
2025-12-09 06:38:25,063 - utils.api - INFO - API call successful, status code: 200
2025-12-09 06:38:25,067 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/cryptocurrencies with params: None
2025-12-09 06:38:26,593 - utils.api - INFO - API call successful, status code: 200
2025-12-09 06:38:26,603 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/payment-methods with params: None
2025-12-09 06:38:26,610 - utils.api - ERROR - HTTP error occurred: 404 Client Error: Not Found for url: http://127.0.0.1:8000/api/v1/payment-methods - For URL: http://127.0.0.1:8000/api/v1/payment-methods
2025-12-09 06:38:26,620 - __main__ - INFO - Fetching BUY offers with filters: {'fiat_code': 'ARS', 'crypto_symbol': 'USDT', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 06:38:26,624 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'ARS', 'crypto_symbol': 'USDT', 'trade_type': 'BUY', 'page': 1, 'page_size': 100}
2025-12-09 06:38:29,907 - utils.api - INFO - API call successful, status code: 200
2025-12-09 06:38:29,913 - __main__ - INFO - Received 100 BUY offers.
2025-12-09 06:38:29,916 - __main__ - INFO - Fetching SELL offers with filters: {'fiat_code': 'ARS', 'crypto_symbol': 'USDT', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 06:38:29,948 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'ARS', 'crypto_symbol': 'USDT', 'trade_type': 'SELL', 'page': 1, 'page_size': 100}
2025-12-09 06:38:32,948 - utils.api - INFO - API call successful, status code: 200
2025-12-09 06:38:32,958 - __main__ - INFO - Received 100 SELL offers.
2025-12-09 06:38:33.080 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 06:38:33.152 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 06:38:34.179 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:22:21,539 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/fiat_currencies with params: None
2025-12-09 07:22:24,663 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:22:24,681 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/cryptocurrencies with params: None
2025-12-09 07:22:26,660 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:22:26,803 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/payment-methods with params: None
2025-12-09 07:22:26,915 - utils.api - ERROR - HTTP error occurred: 404 Client Error: Not Found for url: http://127.0.0.1:8000/api/v1/payment-methods - For URL: http://127.0.0.1:8000/api/v1/payment-methods
2025-12-09 07:22:27,020 - __main__ - INFO - Fetching BUY offers with filters: {'fiat_code': 'COP', 'crypto_symbol': 'USDT', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:22:27,044 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'COP', 'crypto_symbol': 'USDT', 'trade_type': 'BUY', 'page': 1, 'page_size': 100}
2025-12-09 07:22:30,242 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:22:30,257 - __main__ - INFO - Received 100 BUY offers.
2025-12-09 07:22:30,260 - __main__ - INFO - Fetching SELL offers with filters: {'fiat_code': 'COP', 'crypto_symbol': 'USDT', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:22:30,266 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'COP', 'crypto_symbol': 'USDT', 'trade_type': 'SELL', 'page': 1, 'page_size': 100}
2025-12-09 07:22:32,604 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:22:32,619 - __main__ - INFO - Received 100 SELL offers.
2025-12-09 07:22:32.838 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:22:32.906 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:22:33.123 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:22:48,975 - __main__ - INFO - Fetching BUY offers with filters: {'fiat_code': 'VES', 'crypto_symbol': 'USDT', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:22:48,979 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'VES', 'crypto_symbol': 'USDT', 'trade_type': 'BUY', 'page': 1, 'page_size': 100}
2025-12-09 07:22:57,224 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:22:57,233 - __main__ - INFO - Received 100 BUY offers.
2025-12-09 07:22:57,234 - __main__ - INFO - Fetching SELL offers with filters: {'fiat_code': 'VES', 'crypto_symbol': 'USDT', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:22:57,263 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'VES', 'crypto_symbol': 'USDT', 'trade_type': 'SELL', 'page': 1, 'page_size': 100}
2025-12-09 07:23:00,445 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:23:00,451 - __main__ - INFO - Received 100 SELL offers.
2025-12-09 07:23:00.539 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:23:00.568 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:23:00.831 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:52:21,082 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/fiat_currencies with params: None
2025-12-09 07:52:24,872 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:52:24,881 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/cryptocurrencies with params: None
2025-12-09 07:52:28,158 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:52:28,199 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/payment-methods with params: None
2025-12-09 07:52:28,229 - utils.api - ERROR - HTTP error occurred: 404 Client Error: Not Found for url: http://127.0.0.1:8000/api/v1/payment-methods - For URL: http://127.0.0.1:8000/api/v1/payment-methods
2025-12-09 07:52:28,278 - __main__ - INFO - Fetching BUY offers with filters: {'fiat_code': 'VES', 'crypto_symbol': 'DOGE', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:52:28,334 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'VES', 'crypto_symbol': 'DOGE', 'trade_type': 'BUY', 'page': 1, 'page_size': 100}
2025-12-09 07:52:30,595 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:52:30,604 - __main__ - INFO - Received 100 BUY offers.
2025-12-09 07:52:30,605 - __main__ - INFO - Fetching SELL offers with filters: {'fiat_code': 'VES', 'crypto_symbol': 'DOGE', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:52:30,628 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'VES', 'crypto_symbol': 'DOGE', 'trade_type': 'SELL', 'page': 1, 'page_size': 100}
2025-12-09 07:52:32,776 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:52:32,781 - __main__ - INFO - Received 100 SELL offers.
2025-12-09 07:52:32.892 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:52:32.910 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:52:33.091 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:56:55,602 - __main__ - INFO - Fetching BUY offers with filters: {'fiat_code': 'VES', 'crypto_symbol': 'DAI', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:56:55,607 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'VES', 'crypto_symbol': 'DAI', 'trade_type': 'BUY', 'page': 1, 'page_size': 100}
2025-12-09 07:56:58,225 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:56:58,227 - __main__ - INFO - Received 0 BUY offers.
2025-12-09 07:56:58,227 - __main__ - INFO - Fetching SELL offers with filters: {'fiat_code': 'VES', 'crypto_symbol': 'DAI', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:56:58,230 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'VES', 'crypto_symbol': 'DAI', 'trade_type': 'SELL', 'page': 1, 'page_size': 100}
2025-12-09 07:57:00,766 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:57:00,767 - __main__ - INFO - Received 0 SELL offers.
2025-12-09 07:57:33,946 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/fiat_currencies with params: None
2025-12-09 07:57:36,558 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:57:36,592 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/cryptocurrencies with params: None
2025-12-09 07:57:38,779 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:57:38,905 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/payment-methods with params: None
2025-12-09 07:57:38,940 - utils.api - ERROR - HTTP error occurred: 404 Client Error: Not Found for url: http://127.0.0.1:8000/api/v1/payment-methods - For URL: http://127.0.0.1:8000/api/v1/payment-methods
2025-12-09 07:57:39,039 - __main__ - INFO - Fetching BUY offers with filters: {'fiat_code': 'VES', 'crypto_symbol': 'BNB', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:57:39,172 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'VES', 'crypto_symbol': 'BNB', 'trade_type': 'BUY', 'page': 1, 'page_size': 100}
2025-12-09 07:57:41,221 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:57:41,226 - __main__ - INFO - Received 100 BUY offers.
2025-12-09 07:57:41,227 - __main__ - INFO - Fetching SELL offers with filters: {'fiat_code': 'VES', 'crypto_symbol': 'BNB', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 07:57:41,240 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'VES', 'crypto_symbol': 'BNB', 'trade_type': 'SELL', 'page': 1, 'page_size': 100}
2025-12-09 07:57:44,289 - utils.api - INFO - API call successful, status code: 200
2025-12-09 07:57:44,295 - __main__ - INFO - Received 100 SELL offers.
2025-12-09 07:57:44.340 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:57:44.362 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 07:57:44.457 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 10:31:02,311 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/fiat_currencies with params: None
2025-12-09 10:31:05,910 - utils.api - INFO - API call successful, status code: 200
2025-12-09 10:31:05,927 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/cryptocurrencies with params: None
2025-12-09 10:31:08,798 - utils.api - INFO - API call successful, status code: 200
2025-12-09 10:31:08,865 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/payment-methods with params: None
2025-12-09 10:31:08,954 - utils.api - ERROR - HTTP error occurred: 404 Client Error: Not Found for url: http://127.0.0.1:8000/api/v1/payment-methods - For URL: http://127.0.0.1:8000/api/v1/payment-methods
2025-12-09 10:31:09,049 - __main__ - INFO - Fetching BUY offers with filters: {'fiat_code': 'ARS', 'crypto_symbol': 'USDT', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 10:31:09,144 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'ARS', 'crypto_symbol': 'USDT', 'trade_type': 'BUY', 'page': 1, 'page_size': 100}
2025-12-09 10:31:12,238 - utils.api - INFO - API call successful, status code: 200
2025-12-09 10:31:12,244 - __main__ - INFO - Received 100 BUY offers.
2025-12-09 10:31:12,245 - __main__ - INFO - Fetching SELL offers with filters: {'fiat_code': 'ARS', 'crypto_symbol': 'USDT', 'payment_methods': None, 'min_price': None, 'max_price': None}
2025-12-09 10:31:12,249 - utils.api - INFO - Making API call to: http://127.0.0.1:8000/api/v1/offers with params: {'fiat_code': 'ARS', 'crypto_symbol': 'USDT', 'trade_type': 'SELL', 'page': 1, 'page_size': 100}
2025-12-09 10:31:15,884 - utils.api - INFO - API call successful, status code: 200
2025-12-09 10:31:15,891 - __main__ - INFO - Received 100 SELL offers.
2025-12-09 10:31:15.955 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 10:31:15.971 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.        
2025-12-09 10:31:16.054 Please replace `use_container_width` with `width`.

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`. 

(By the other hand when i am in trader dashboard page and open advanced settings this error appears
HTTP error occurred: 404 Client Error: Not Found for url: http://127.0.0.1:8000/api/v1/payment-methods - Check if the API is running and the endpoint is correct.)




  # Api Behavior (All ok)

(.venv) PS C:\Users\DELL\Desktop\dashboards> python run_api.py
Starting API server...
INFO:     Will watch for changes in these directories: ['C:\\Users\\DELL\\Desktop\\dashboards\\Api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [26640] using WatchFiles
INFO:     Started server process [22124]
INFO:     Waiting for application startup.
2025-12-09 06:35:56,116 | INFO | Api.p2p_api.main | Starting P2P Dashboard API...
INFO:     Application startup complete.