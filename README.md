# COVID-19 Hyogo

Tracking the COVID-19 outbreak in Hyogo Prefecture, Japan at
[https://covid-hyogo.now.sh/][0]

This project consists of a somewhat opinionated set of charts inspired by
[17 (or so) responsible live visualizations about the coronavirus][1]. The
main ideas are:

1. The number of confirmed cases should not be shown in red
   (contracting the virus is not a death sentence).
1. Absolute numbers should be countered with reference
   (relative numbers provide more context).
1. Cumulative cases should be avoided in charts
   (there are people on track to recovery).
1. Choropleth maps are avoided if they are necessary at all
   (there are already maps showing almost all countries in red, but
   they all seem out of proportion).

All data except otherwise noted are retrieved from the official website of the
Hyogo Prefectural Government, particularly:

1. [新型コロナウイルスに感染した患者の発生状況][2]
1. [新型コロナウイルスに感染した患者の状況][3]
1. [新型コロナウイルス感染症の県内検査状況について][4]

## Usage

This project uses [node](http://nodejs.org) and [npm](https://npmjs.com).
Go check them out if you don't have them locally installed.

To run a local development server at `localhost:8080`:

```sh
yarn serve
```

To build for production:

```sh
yarn build
```

Lint and fix your code before building:

```sh
yarn format
```

## Contributing

Comments and contributions welcome! Please [submit an issue][5] or send a
pull request directly.

## Built with

* [Vue.js](https://vuejs.org/index.html) - The Progressive JavaScript Framework
* [Chart.js](https://www.chartjs.org/) - Simple yet flexible JavaScript
  charting for designers & developers
* [Leaflet](https://leafletjs.com/) - An open-source JavaScript library
   for mobile-friendly interactive maps
* And many great open source software.

## License

This project is licensed under the MIT License

[0]: https://covid-hyogo.now.sh/
[1]: https://blog.datawrapper.de/coronaviruscharts/
[2]: https://web.pref.hyogo.lg.jp/kk03/corona_hasseijyokyo.html
[3]: https://web.pref.hyogo.lg.jp/kk03/corona_kanjyajyokyo.html
[4]: https://web.pref.hyogo.lg.jp/kf16/singatakoronakensa.html
[5]: https://github.com/hktang/covid-hyogo/issues
