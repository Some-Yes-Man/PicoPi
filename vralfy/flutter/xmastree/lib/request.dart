import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:xmastree/webresponse.dart';

class Request {
  static final HttpClient client = HttpClient();

  static Future<WebResponse> runGetRequest(String url, Map<String, dynamic>? arguments) async {
    String parameter = (arguments ?? {}) //
        .map((key, value) => MapEntry(key, value is Map || value is List ? jsonEncode(value) : value)) //
        .map((key, value) => MapEntry(Uri.encodeQueryComponent(key), Uri.encodeQueryComponent('$value'))) //
        .map((key, value) => MapEntry(key, '$key=$value')) //
        .values
        .join('&');

    stdout.writeln('$url?$parameter');
    HttpClientRequest request = await client.getUrl(Uri.parse('http://$url?$parameter'));
    HttpClientResponse response = await request.close();

    if (response.statusCode == 200) {
      String body = await response.transform(utf8.decoder).join();
      stdout.writeln(body);
      return WebResponse.fromJson(jsonDecode(body));
    } else {
      throw Exception('Failed to load url: $url');
    }
  }
}
