{ pkgs ? import <nixpkgs> {  } }:

let
  python36-beverages-tracker = pkgs.python36.withPackages (p: with p; [
    requests
    tkinter
    pyqt5
    flask
    numpy
    matplotlib
  ]);
in

pkgs.stdenvNoCC.mkDerivation {
  name = "python36-beverages-tracker";
  nativeBuildInputs = with pkgs; [
    python36-beverages-tracker
    qt5Full
  ];
}


