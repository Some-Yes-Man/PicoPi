import 'dart:io';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:xmastree/request.dart';
import 'package:xmastree/scrollcontainer.dart';
import 'package:xmastree/webresponse.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'XmasTree',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  static SharedPreferences? pref;
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  WebResponse? serverList;
  static final Map<String, dynamic> defaultsStr = {
    'renderer': '0',
  };
  static final Map<String, dynamic> defaultsInt = {
    'red': 255,
    'green': 255,
    'blue': 255,
    'deviationRed': 0,
    'deviationGreen': 0,
    'deviationBlue': 0,
    'deviationRedPos': 0,
    'deviationGreenPos': 0,
    'deviationBluePos': 0,
    'deviationRedNeg': 0,
    'deviationGreenNeg': 0,
    'deviationBlueNeg': 0,
    'stars': 25,
    'length': 5,
    'fade': 0,
    'minFade': 100,
    'maxFade': 300,
    'duration': 250,
    'minDuration': 50,
    'maxDuration': 150,
  };

  @override
  Widget build(BuildContext context) {
    if (MyHomePage.pref == null) {
      SharedPreferences.getInstance().then((value) => setState(() {
            MyHomePage.pref = value;
            setState(() {});
          }));
      return Column();
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text(''),
      ),
      floatingActionButton: serverList == null
          ? null
          : FloatingActionButton(
              onPressed: () async {
                await Request.runGetRequest(ip, {...defaultsStr, ...defaultsInt});
                Request.runGetRequest(ip, {
                  ...defaultsStr.map((key, value) => MapEntry(key, MyHomePage.pref?.getString(key) ?? value)),
                  ...defaultsInt.map((key, value) => MapEntry(key, MyHomePage.pref?.getInt(key) ?? value)),
                });
              },
              tooltip: 'Save',
              child: const Icon(Icons.save),
            ),
      body: ScrollContainer(
        header: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextFormField(
              decoration: const InputDecoration(labelText: 'IP'),
              initialValue: ip,
              onChanged: (value) => setState(() {
                MyHomePage.pref?.setString('IP', value);
              }),
            ),
            ElevatedButton(
              onPressed: () => Request.runGetRequest(ip, {'list': null}).then((value) => setState(() => serverList = value)),
              child: const Text('update'),
            ),
          ],
        ),
        footer: Column(children: [
          ...info,
        ]),
        child: Column(children: [
          ...parameter,
        ]),
      ),
    );
  }

  String get ip {
    return MyHomePage.pref?.getString('IP') ?? '192.168.0.100';
  }

  List<Widget> get info {
    List<Widget> ret = [];
    if (serverList == null) {
      return ret;
    }

    ret.add(const Text('Info'));
    ret.add(const Divider());
    ret.add(Table(
      children: [
        TableRow(children: [
          const TableCell(child: Text('LEDs')),
          TableCell(child: Text('${serverList?.leds ?? ''}')),
        ]),
        TableRow(children: [
          const TableCell(child: Text('Muster')),
          TableCell(child: Text(serverList?.current_renderer ?? '')),
        ]),
      ],
    ));

    return ret;
  }

  List<Widget> get parameter {
    List<Widget> ret = [];
    if (serverList == null) {
      return ret;
    }

    ret.add(const Text('Parameter'));
    ret.add(const Divider());
    String current_renderer = '0';
    (serverList?.renderer ?? {}).forEach((key, value) => current_renderer = (value == serverList?.current_renderer ? key : current_renderer));
    MyHomePage.pref?.setString('renderer', MyHomePage.pref?.getString('renderer') ?? current_renderer);

    ret.add(DropdownButton(
      value: MyHomePage.pref?.getString('renderer') ?? current_renderer,
      items: (serverList?.renderer ?? {})
          .map(
            (key, value) => MapEntry(
                key,
                DropdownMenuItem<String>(
                  value: key,
                  child: Text(value),
                )),
          )
          .values
          .toList(),
      onChanged: (v) {
        MyHomePage.pref?.setString('renderer', v as String).then((value) => setState(() {}));
      },
    ));
    ret.addAll(parameterLed);
    ret.addAll(parameterColor);
    ret.addAll(parameterDuration());

    return ret;
  }

  List<Widget> get parameterColor {
    return [
      'red',
      'green',
      'blue',
      'deviationRed',
      'deviationGreen',
      'deviationBlue',
      'deviationRedPos',
      'deviationGreenPos',
      'deviationBluePos',
      'deviationRedNeg',
      'deviationGreenNeg',
      'deviationBlueNeg',
    ]
        .map(
          (colorName) => Column(
            children: [
              Text('$colorName: ${MyHomePage.pref?.getInt(colorName) ?? (defaultsInt[colorName] ?? 0)}'),
              Slider(
                value: (MyHomePage.pref?.getInt(colorName) ?? (defaultsInt[colorName] ?? 0)).toDouble(),
                min: 0,
                max: 255,
                onChanged: (v) {
                  MyHomePage.pref?.setInt(colorName, v.floor());
                  setState(() {});
                },
              ),
            ],
          ),
        )
        .toList();
  }

  List<Widget> get parameterLed {
    return [
      'stars',
      'length',
    ]
        .map(
          (colorName) => Column(
            children: [
              Text('$colorName: ${MyHomePage.pref?.getInt(colorName) ?? (defaultsInt[colorName] ?? 0)}'),
              Slider(
                value: (MyHomePage.pref?.getInt(colorName) ?? (defaultsInt[colorName] ?? 0)).toDouble(),
                min: 0,
                max: (serverList?.leds ?? 50).toDouble(),
                onChanged: (v) {
                  MyHomePage.pref?.setInt(colorName, v.floor());
                  setState(() {});
                },
              ),
            ],
          ),
        )
        .toList();
  }

  List<Widget> parameterDuration({int min = 0, int max = 500}) {
    return [
      'duration',
      'minDuration',
      'maxDuration',
      'fade',
      'minFade',
      'maxFade',
    ]
        .map(
          (colorName) => Column(
            children: [
              Text('$colorName: ${MyHomePage.pref?.getInt(colorName) ?? (defaultsInt[colorName] ?? 0)}'),
              Slider(
                value: (MyHomePage.pref?.getInt(colorName) ?? (defaultsInt[colorName] ?? 0)).toDouble(),
                min: min.toDouble(),
                max: max.toDouble(),
                onChanged: (v) {
                  MyHomePage.pref?.setInt(colorName, v.floor());
                  setState(() {});
                },
              ),
            ],
          ),
        )
        .toList();
  }
}
