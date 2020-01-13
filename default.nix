{ pkgs ? import <nixpkgs> {  } }:

let
  python37-beverages-tracker = pkgs.python37.withPackages (p: with p; [
    requests
    tkinter
    flask
    numpy
    mysql-connector
    matplotlib
  ]);
in

pkgs.stdenvNoCC.mkDerivation {
  name = "python37-beverages-tracker";
  nativeBuildInputs = with pkgs; [
    python37-beverages-tracker
  ];
}


