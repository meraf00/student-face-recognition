import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
class FaceMainScreen extends StatefulWidget {
  const FaceMainScreen({super.key, required this.title});


  final String title;

  @override
  State<FaceMainScreen> createState() => _FaceMainScreenState();
}

class _FaceMainScreenState extends State<FaceMainScreen> {


  File? image;

  Future pickImage(int source) async {
    try{
      final image = await ImagePicker().pickImage(source: source==0? ImageSource.gallery : ImageSource.camera);
      if (image==null) return;

      final imageTemp = File(image.path);
      setState(() => this.image = imageTemp);
    }
    catch(e){
      print("Failed to pick image");
    }

  }
  Future<void> uploadImage(File imageFile) async {
    // Replace 'your_api_endpoint' with the actual API endpoint
    var apiUrl = Uri.parse('https://api-us.faceplusplus.com/facepp/v3/detect?api_key=v-4SD9ao-Azt0qzZDExzIpLDcurWXOFz&api_secret=GZIGfGLo2iSKCJmeYRguW70LtugeBLpc');

    // Create a multipart request
    var request = http.MultipartRequest('POST', apiUrl);

    // Attach the image file to the request
    var fileStream = http.ByteStream(imageFile.openRead());
    var length = await imageFile.length();
    var multipartFile = http.MultipartFile('image_file', fileStream, length,);
    request.files.add(multipartFile);

    // Send the request
    var response = await request.send();
    print(response);
    // Check the response
    if (response.statusCode == 200) {
      print('Image uploaded successfully');
    } else {
      print('Failed to upload image. Status code: ${response.statusCode}');
    }
  }



  @override
  Widget build(BuildContext context) {

    return Scaffold(
        body: Container(
          width: double.infinity,
          decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.bottomLeft, end: Alignment.topRight,
                colors: [ Color(0xFF292734), Color(0xFF000000)],
                stops: [-0.0944, 1.0],
                transform: GradientRotation(170 * (3.1415926535 / 180)),)),
          child: SafeArea(
              child: Column(

                children: [
                  const SizedBox(height: 65,),
                  Text("Welcome", textAlign: TextAlign.center, style: Theme.of(context).textTheme.headlineSmall!.copyWith(fontWeight: FontWeight.w500, color: Colors.white),),
                  const Spacer(),
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: image !=null ? Image.file(image!, width: 320,height: 320,): Image.asset("assets/empty.png", width: 300, height: 300,)
                  ) ,
                  const Spacer(),
                  image == null ?
                  Column(
                    children: [
                      ElevatedButton(
                        onPressed: (){pickImage(0);},
                        style: ElevatedButton.styleFrom(
                          fixedSize: const Size(270, 26), // Adjust the width and height as needed
                        ),
                        child: const Text('Upload Image From Gallery'),
                      ),
                      const SizedBox(height: 10,),
                      ElevatedButton(
                        onPressed: (){pickImage(1);},
                        style: ElevatedButton.styleFrom(
                          fixedSize: const Size(270, 26), // Adjust the width and height as needed
                        ),
                        child: const Text('Take a Camera capture'),
                      ),
                    ],
                  ) : ElevatedButton(
                            onPressed: (){
                            //   sending it to backend
                              uploadImage(image!);
                            },
                            style: ElevatedButton.styleFrom(
                              fixedSize: const Size(270, 26), // Adjust the width and height as needed
                            ),
                            child: const Text('Send'),),
                  const SizedBox(height: 90,),
                ],
              )
          ),
        )
    );
  }
}


// Center(
// child: Column(
// children: [
// MaterialButton(
// color: Colors.blueAccent, onPressed: (){pickImage(0);},
// child: const Text("From Gallery")),
// MaterialButton(
// color: Colors.blueAccent, onPressed: (){pickImage(1);},
// child: const Text("From Camera")),
//
// const SizedBox(height: 20,),
//
// image !=null ? Image.file(image!) : const Text("No image Selected")
// ],
// ),
// )