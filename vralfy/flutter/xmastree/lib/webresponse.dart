import 'package:json_annotation/json_annotation.dart';

part 'webresponse.g.dart';

@JsonSerializable()
class WebResponse {
  @JsonKey(defaultValue: '')
  final String request_str;
  @JsonKey(defaultValue: [])
  final List<String> request;
  @JsonKey(defaultValue: {})
  final Map<String, String> header;
  @JsonKey(defaultValue: [])
  final List<String> GET;
  @JsonKey(defaultValue: [])
  final List<String> POST;
  @JsonKey(defaultValue: {})
  final Map<String, String> parameter;

  @JsonKey(defaultValue: 0)
  final int leds;
  @JsonKey(defaultValue: '')
  final String current_renderer;
  @JsonKey(defaultValue: {})
  final Map<String, String> renderer;
  @JsonKey(defaultValue: {})
  final Map<String, dynamic> renderer_parameter;

  WebResponse({
    required this.request,
    required this.request_str,
    required this.header,
    required this.GET,
    required this.POST,
    required this.parameter,
    required this.leds,
    required this.current_renderer,
    required this.renderer,
    required this.renderer_parameter,
  });

  factory WebResponse.fromJson(Map<String, dynamic> json) => _$WebResponseFromJson(json);
  Map<String, dynamic> toJson() => _$WebResponseToJson(this);
}
