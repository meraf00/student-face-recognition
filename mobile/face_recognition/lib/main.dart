import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'config.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Image  App',
      theme: ThemeData(
        primaryColor: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  File? _imageFile;
  final picker = ImagePicker();
  String _serverResponse = '';

  Future getImage(ImageSource source) async {
    final pickedFile = await picker.pickImage(source: source);

    setState(() {
      if (pickedFile != null) {
        _imageFile = File(pickedFile.path);
      }
    });
  }

  Future<void> sendImageToBackend(File imageFile) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));

      request.files
          .add(await http.MultipartFile.fromPath('file', imageFile.path));

      // Send the request
      var response = await request.send();

      String responseBody = await response.stream.bytesToString();
      Map<String, dynamic> jsonResponse = json.decode(responseBody);

      if (response.statusCode == 200) {
        setState(() {
          _serverResponse = jsonResponse['result'];
        });
      } else {
        setState(() {
          _serverResponse =
              'Failed to send image. Status code: ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _serverResponse = 'Error sending image: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Center(child: Text('Face Recognition')),
      ),
      body: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 40),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: <Widget>[
              Expanded(
                child: _imageFile == null
                    ? const Center(child: Text('No image selected.'))
                    : Image.file(_imageFile!),
              ),
              if (_serverResponse.isNotEmpty)
                Text(
                  _serverResponse,
                  style: const TextStyle(
                    color: Colors.green,
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                  ),
                ),
              const SizedBox(
                height: 20,
              ),
              Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton(
                        onPressed: () async {
                          await getImage(ImageSource.gallery);
                          if (_imageFile != null) {
                            await sendImageToBackend(_imageFile!);
                          }
                        },
                        child: const Row(children: [
                          Icon(Icons.image, size: 20),
                          SizedBox(width: 5),
                          Text('Gallery')
                        ]),
                      ),
                      const SizedBox(width: 20),
                      ElevatedButton(
                        onPressed: () async {
                          await getImage(ImageSource.camera);
                          if (_imageFile != null) {
                            await sendImageToBackend(_imageFile!);
                          }
                        },
                        child: const Row(children: [
                          Icon(Icons.camera, size: 20),
                          SizedBox(width: 5),
                          Text('Camera')
                        ]),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                ],
              ),
            ],
          )),
    );
  }
}
