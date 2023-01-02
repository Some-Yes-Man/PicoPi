// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'webresponse.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

WebResponse _$WebResponseFromJson(Map<String, dynamic> json) => WebResponse(
      request: (json['request'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
      request_str: json['request_str'] as String? ?? '',
      header: (json['header'] as Map<String, dynamic>?)?.map(
            (k, e) => MapEntry(k, e as String),
          ) ??
          {},
      GET: (json['GET'] as List<dynamic>?)?.map((e) => e as String).toList() ??
          [],
      POST:
          (json['POST'] as List<dynamic>?)?.map((e) => e as String).toList() ??
              [],
      parameter: (json['parameter'] as Map<String, dynamic>?)?.map(
            (k, e) => MapEntry(k, e as String),
          ) ??
          {},
      leds: json['leds'] as int? ?? 0,
      current_renderer: json['current_renderer'] as String? ?? '',
      renderer: (json['renderer'] as Map<String, dynamic>?)?.map(
            (k, e) => MapEntry(k, e as String),
          ) ??
          {},
      renderer_parameter:
          json['renderer_parameter'] as Map<String, dynamic>? ?? {},
    );

Map<String, dynamic> _$WebResponseToJson(WebResponse instance) =>
    <String, dynamic>{
      'request_str': instance.request_str,
      'request': instance.request,
      'header': instance.header,
      'GET': instance.GET,
      'POST': instance.POST,
      'parameter': instance.parameter,
      'leds': instance.leds,
      'current_renderer': instance.current_renderer,
      'renderer': instance.renderer,
      'renderer_parameter': instance.renderer_parameter,
    };
