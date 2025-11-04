import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Wikiwhat?',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: GameScreen(),
    );
  }
}

class GameScreen extends StatefulWidget {
  @override
  _GameScreenState createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  final TextEditingController _controller = TextEditingController();
  final FocusNode _focusNode = FocusNode();

  String _articleTitle = 'Exemple'; // Le titre correct
  String _articleContent =
      'Ceci est le contenu de l\'article à deviner. Les mots sont cachés.';
  List<String> _foundWords = [];
  bool _gameWon = false;
  bool _errorFlash = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      FocusScope.of(context).requestFocus(_focusNode);
    });
  }

  String _caviardeTitle(String title) {
    return title.replaceAll(RegExp(r'.'), '•'); // masque toutes les lettres
  }

  void _checkInput(String input) {
    String normalizedInput = input.toLowerCase().trim();
    if (normalizedInput == _articleTitle.toLowerCase()) {
      setState(() {
        _gameWon = true;
      });
    } else if (!_foundWords.contains(normalizedInput)) {
      setState(() {
        _errorFlash = true;
      });
      Future.delayed(Duration(milliseconds: 200), () {
        setState(() {
          _errorFlash = false;
        });
      });
    }
    _controller.clear();
    FocusScope.of(context).requestFocus(_focusNode);
  }

  void _newArticle() {
    setState(() {
      _articleTitle = 'NouveauTitre';
      _articleContent = 'Voici un nouvel article à deviner.';
      _foundWords.clear();
      _gameWon = false;
      _controller.clear();
      FocusScope.of(context).requestFocus(_focusNode);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Wikiwhat?')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(
              _gameWon ? _articleTitle : _caviardeTitle(_articleTitle),
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            Expanded(
              child: SingleChildScrollView(
                child: Text(
                  _articleContent,
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
            AnimatedContainer(
              duration: Duration(milliseconds: 200),
              decoration: BoxDecoration(
                border: Border.all(
                    color: _errorFlash ? Colors.red : Colors.grey, width: 2),
                borderRadius: BorderRadius.circular(5),
              ),
              padding: EdgeInsets.symmetric(horizontal: 8),
              child: TextField(
                controller: _controller,
                focusNode: _focusNode,
                onSubmitted: _checkInput,
                decoration: InputDecoration(
                  border: InputBorder.none,
                  hintText: 'Tapez le titre ici...',
                ),
              ),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: _newArticle,
              child: Text('Nouvel article'),
            ),
            if (_gameWon)
              Padding(
                padding: const EdgeInsets.only(top: 10),
                child: Text(
                  'Bravo ! Article trouvé !',
                  style: TextStyle(fontSize: 20, color: Colors.green),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
