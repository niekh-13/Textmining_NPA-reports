#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES=/home/niek/Documents/minor_intern/Bijlage_clean/*
for f in $FILES
do
  echo "$f"
 if ! isutf8 -q "$f"; then
#    awk '{sub(/Patiënt/, "Patient")}1' "$f" > temp.txt && mv temp.txt "$f"
#    awk '{sub(/patiënt/, "patient")}1' "$f" > temp.txt && mv temp.txt "$f"
   iconv --from-code=ISO-8859-15 --to-code=UTF-8 "$f" > temp.txt && mv temp.txt "$f"
 fi

  awk '{sub(/Pre-meting/, "PRE-meting")}1' "$f" > temp.txt && mv temp.txt "$f"

  awk '{sub(/12 maanden Meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12 maanden meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12 maandenmeting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12 maanden-meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12maanden meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12 maanden post meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12-post meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12post meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12 maanden post-meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/12-maanden meting/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/T12:/, "12 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"

  awk '{sub(/6 maandenPOST/, "6 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/6 maanden-POST/, "6 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/6-maanden POST/, "6 maanden POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Algemenen observatie:/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Algem-ene observatie:/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Algemene observatie/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Algemene observatie::/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Algemene observatie (digitaal):/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Algemene observatie(digitaal):/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/ë/, "e")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Testobservaties:/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Testobservatie:/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Testobservaties/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Testobservatie/, "Algemene observatie:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Rapportage dor patient:/, "Gerapporteerde klachten door patient:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Gerapporteerde klachten door patiente:/, "Gerapporteerde klachten door patient:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Zelfrapportage:/, "Gerapporteerde klachten door patient:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/\[ten tijde van PRE-, POST-meting\]/, "")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/Overige opvallende kenmerken: \)/, "Overige opvallende kenmerken:")}1' "$f" > temp.txt && mv temp.txt "$f"
  awk '{sub(/\( Presentatie: /, "Presentatie: ")}1' "$f" > temp.txt && mv temp.txt "$f"
done
