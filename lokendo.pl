#!/usr/bin/perl

use LWP::UserAgent;
use Getopt::Long;

use feature "say";
my $ua = LWP::UserAgent->new;
do "$ENV{HOME}/.config/lokendo/config.pl";

GetOptions ("voz=s"         => \$voz, # Voz
            "velocidad=s"   => \$rate, # Velocidad de hablar
		  "v=s"           => \$voz, # Voz
		  "r=i"           => \$rate, # velocidad
		  "srate=i"       => \$srate, # Sample Rate
		  "pitch=f"       => \$pitch, # Semitonos
		  "m"             => \$musica, # Musica de fondo
		  "h"             => \$help # Ayuda
		 );

sub help() {
  say "Este programa coge el STDIN y escupe el STDOUT con Loquendo según el archivo de configuración o los parámetros";
  say "EJEMPLOS:";
  say "echo \"Hola culeros les saluda el anticristo\" | perl loquendo.pl > anticristo.wav: Archivo a .wav";
  say "echo \"Esto es una crítica a los pinches otakus\" | perl loquendo.pl --voice=Carlos| mpv /dev/stdin: Ejecutar en mpv con la voz de Carlos";
  say "echo \"Putos de mierda XDXDXD\" | perl loquendo.pl --pitch=2 > archivo.wav: aumentar la voz 2 semitonos";
  say "echo \"Putos de mierda XDXDXD\" | perl loquendo.pl --pitch=-2 > archivo.wav: bajar la voz 2 semitonos";
  say "echo \"Putos de mierda XDXDXD\" | perl loquendo.pl --srate=8000 --voice=Juan > archivo.wav: Que la voz de Juan se escuche a culo";
  say "--voz:  La voz que usar";
  say "--srate: Sample rate";
  say "-m: poner la musica de fondo de Loquendo";
  say "--velocidad palabras por minuto";
  say "--pitch semitonos a aumentar o disminuir"
}

if($help) {
  help();
  exit;
}

$rate = 160 if $voz eq "Juan" and $rate == 200;
print <STDERR>, $velocidad;
undef $/;
my $texto = <STDIN>;
my %form = (
		  voz => $voz,
		  velocidad => $rate,
		  texto => $texto
		 );

my $file = sprintf "%08X.wav", rand(0xffffffff);
open(my $fh, ">:raw","/tmp/$file");
my $res = $ua->post("$loquendo_instance/generar", \%form);
print $fh $res->content;
close($fh);


if ($pitch != 0 ) {
  my $rpitch = $pitch * 100;
  `sox  /tmp/$file /tmp/output.wav pitch $rpitch`;
  rename("/tmp/output.wav","/tmp/$file");
}
if ($srate != 22025) {
  `sox --no-show-progress /tmp/$file -r $srate /tmp/output.wav`;
  rename("/tmp/output.wav","/tmp/$file");
}

if ($musica) {
  `ffmpeg -hide_banner -loglevel error -i /tmp/$file -stream_loop -1 -i /home/anon/lokendo.wav -filter_complex amix=inputs=2:duration=first:dropout_transition=1 /tmp/output.wav`;
  rename("/tmp/output.wav","/tmp/$file");
}

my $archivo = "/tmp/$file";
open my $fh2, '<', $archivo or die "No se puede abrir $archivo: $!";
  
local $/;			    # esto hace que <FILEHANDLE> lea todo de golpe
my $contenido = <$fh2>;
print $contenido;
close $fh2;

