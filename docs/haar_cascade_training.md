# Treinar HAAR Cascade
## 1 - Preparar imagens negativas
Para treinar o filtro HAAR será necessário uma grande quantidade das chamadas
imagens negativas, são imagens diversas que **NÃO** podem conter o objeto que
se deseja localizar.

É necessário uma grande quantidade de imagens negativas, ao menos 2 mil.

## 2 - Preparar imagens positivas
### Obter imagens objeto
* Iluminação
* Angulo
* Qualidade

### Recortar e adicionar fundo branco
* GIMP

### Mesclar imagens positiva com imagens negativas de background
```ps
opencv_createsamples.exe -img C:\Daniel\Code\LIA\placas_cropped\pare_4.jpg -bg C:\Daniel\Code\LIA\n\negatives.txt -info C:\Daniel\Code\LIA\samples_4\pare.txt -num 1000 -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.4 -bgcolor 255 -bgthresh 8 -w 48 -h 48
```

### Recortar objeto da imagem mesclada
* Cascade-trainer-GUI

## 3 - Treinando
* Cascade-trainer-GUI
