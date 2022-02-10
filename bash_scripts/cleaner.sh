#!/bin/bash

#arguments
while getopts i:o: flag
do
    case "${flag}" in
        i) input_dir=${OPTARG};;
        o) output_dir=${OPTARG};;
    esac
done

#mv medical note files to be cleaned for parser to output dir
cp $input_dir/* $output_dir

#loop over files
for f in $output_dir/*
do
    echo "$f"
    #check if file has UTF-8 encoding otherwise change to UTF-8 but before change special character
    if ! isutf8 -q "$f"; then
        sed -e 'y/$ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöøùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĴĵĶķĹĺĻļĽľĿŀŁłŃńŅņŇňŉŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſƒƠơƯưǍǎǏǐǑǒǓǔǕǖǗǘǙǚǛǜǺǻǾǿ/SAAAAAACEEEEIIIIDNOOOOOOUUUUYsaaaaaaceeeeiiiinoooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIijKkLlLlLlLlllNnNnNnnOoOoOoORrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzsfOoUuAaIiOoUuUuUuUuUuAaOo/' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/Ǽ/,"AE")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/ǽ/,"ae")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/Œ/,"AE")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/œ/,"ae")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/Æ/,"AE")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/æ/,"ae")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/Ĳ/,"IJ")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/ĳ/,"ij")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/Ã¨/,"e")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/Ãª/,"e")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/Ã©/,"e")}1' "$f" > temp.txt && mv temp.txt "$f"

        iconv --from-code=ISO-8859-15 --to-code=UTF-8 "$f" > temp.txt && mv temp.txt "$f"
    else
        awk '{sub(/Pre/, "PRE")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/pre/, "PRE")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/PRE/, "PRE-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/PRE-meting-meting/, "PRE-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/post/, "POST")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/POST/, "POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
        awk '{sub(/POST-meting-meting/, "POST-meting")}1' "$f" > temp.txt && mv temp.txt "$f"
    fi

    sed -e 'y/$ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöøùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĴĵĶķĹĺĻļĽľĿŀŁłŃńŅņŇňŉŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſƒƠơƯưǍǎǏǐǑǒǓǔǕǖǗǘǙǚǛǜǺǻǾǿ/SAAAAAACEEEEIIIIDNOOOOOOUUUUYsaaaaaaceeeeiiiinoooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIijKkLlLlLlLlllNnNnNnnOoOoOoORrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzsfOoUuAaIiOoUuUuUuUuUuAaOo/' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/Ǽ/,"AE")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/ǽ/,"ae")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/Œ/,"AE")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/œ/,"ae")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/Æ/,"AE")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/æ/,"ae")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/Ĳ/,"IJ")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/ĳ/,"ij")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/Ã¨/,"e")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/Ãª/,"e")}1' "$f" > temp.txt && mv temp.txt "$f"
    awk '{sub(/Ã©/,"e")}1' "$f" > temp.txt && mv temp.txt "$f"


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
