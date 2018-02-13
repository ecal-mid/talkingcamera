CAPTION=$(cat _caption_output/latest.txt)
echo $CAPTION
CAPTION=$(translate-cli -o -t "fr" "$CAPTION")
#echo $TEXT_TRANSLATED
#gtts-cli.py "$(cat _caption_output/latest.txt)" -l "en" -o test.mp3
gtts-cli.py "$CAPTION" -l "en" -o test.mp3
afplay test.mp3
rm test.mp3
