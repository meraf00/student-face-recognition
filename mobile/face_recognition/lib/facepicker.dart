import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;

class FaceDetectionApp extends StatefulWidget {
  @override
  _FaceDetectionAppState createState() => _FaceDetectionAppState();
}

class _FaceDetectionAppState extends State<FaceDetectionApp> {
  final picker = ImagePicker();

  Future<void> _getImageAndDetect() async {
    // final pickedFile = await picker.getImage(source: ImageSource.gallery);
    //
    // if (pickedFile != null) {
    //   // Upload the image to Hugging Face and get predictions
    //   final predictions = await _getFacePredictions(pickedFile.path);
    //
    //   // Display the predictions or similar face in your app
    //   // Update UI accordingly
    // }
  }

  Future<List<dynamic>?> _getFacePredictions(String imagePath) async {
    final response = await http.post(
      Uri(path: "http://localhost:3000/face"),
      body: {'image_path': imagePath},
    );

    if (response.statusCode == 200) {
      // Parse the response and return predictions
      // return parseResponse(response.body);
    } else {
      throw Exception('Failed to load predictions');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Face Detection App'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: _getImageAndDetect,
          child: Text('Upload Image and Detect Face'),
        ),
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: FaceDetectionApp(),
  ));
}
