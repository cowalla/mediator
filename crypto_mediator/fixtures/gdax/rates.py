request_url = lambda x: 'https://api.coinbasepro.com/products/{product_id}/candles'.format(product_id=x)


def response(product_id, **kwargs):
        return [
                [1517089620, 1104.98, 1104.99, 1104.99, 1104.99, 10.5441164],
                [1517089560, 1104.5, 1104.99, 1104.5, 1104.99, 8.14463178],
                [1517089500, 1103, 1104.41, 1103, 1104.41, 22.614476099999994],
                [1517089440, 1102.99, 1103, 1103, 1103, 23.13939054], [1517089380, 1102.99, 1103, 1103, 1103, 19.16080255],
                [1517089320, 1102.99, 1105.41, 1105.41, 1103, 17.80409762],
                [1517089260, 1105.4, 1105.7, 1105.7, 1105.4, 10.73515623],
                [1517089200, 1105.69, 1105.71, 1105.71, 1105.69, 38.54485796000001],
                [1517089140, 1105.01, 1105.71, 1105.01, 1105.71, 170.76249532999998],
                [1517089080, 1105, 1105.71, 1105.7, 1105.01, 37.063444249999996],
                [1517089020, 1105.7, 1105.71, 1105.71, 1105.7, 13.75961801],
                [1517088960, 1104.99, 1105.71, 1105, 1105.71, 18.32040526],
                [1517088900, 1102.99, 1105, 1103, 1105, 49.14769911],
                [1517088840, 1100, 1102.99, 1100, 1102.99, 26.140454590000004],
                [1517088780, 1099, 1100, 1099, 1100, 21.79406457], [1517088720, 1098.92, 1099, 1098.92, 1099, 29.76049659],
                [1517088660, 1098.64, 1098.93, 1098.65, 1098.93, 25.92489062],
                [1517088600, 1097.43, 1098.65, 1098.65, 1098.6, 18.51707688],
                [1517088540, 1098.56, 1098.93, 1098.92, 1098.56, 30.006206249999998],
                [1517088480, 1098.92, 1098.93, 1098.93, 1098.93, 27.761804129999998],
                [1517088420, 1098.53, 1098.95, 1098.95, 1098.92, 6.98594914],
                [1517088360, 1098.94, 1098.96, 1098.95, 1098.95, 11.88825363],
                [1517088300, 1098.95, 1098.96, 1098.95, 1098.96, 13.893805839999999],
                [1517088240, 1098.95, 1099, 1098.99, 1098.95, 31.486315949999995],
                [1517088180, 1098.99, 1099, 1099, 1099, 31.757823539999997],
                [1517088120, 1097.41, 1099.41, 1097.99, 1099, 31.18628613],
                [1517088060, 1097.04, 1100.49, 1100.49, 1097.79, 35.13729797],
                [1517088000, 1100.49, 1101.31, 1101.3, 1100.49, 19.791848809999998],
                [1517087940, 1101.3, 1102.16, 1102.16, 1101.68, 15.0837899],
                [1517087880, 1102.15, 1102.17, 1102.16, 1102.17, 21.01694959],
                [1517087820, 1100.23, 1102.16, 1100.23, 1102.16, 37.514550199999995],
                [1517087760, 1100, 1100.28, 1100.26, 1100.28, 47.50495729],
                [1517087700, 1100, 1100.26, 1100, 1100.25, 33.17890205],
                [1517087640, 1100, 1100.78, 1100.77, 1100, 34.27802839],
                [1517087580, 1100.77, 1101.01, 1101, 1100.77, 36.00361046],
                [1517087520, 1101, 1101.33, 1101.33, 1101, 58.942644259999994],
                [1517087460, 1101.33, 1104.49, 1104.49, 1101.33, 64.35714632999999],
                [1517087400, 1104.49, 1104.5, 1104.5, 1104.49, 71.68365268],
                [1517087340, 1104.49, 1104.5, 1104.49, 1104.49, 31.93530212],
                [1517087280, 1104.49, 1104.5, 1104.49, 1104.49, 52.58420323000001],
                [1517087220, 1104.49, 1105.01, 1105, 1104.49, 16.42757737],
                [1517087160, 1105, 1105.76, 1105.75, 1105, 54.81004853],
                [1517087100, 1105.75, 1105.76, 1105.75, 1105.75, 30.62521826],
                [1517087040, 1105.49, 1105.76, 1105.5, 1105.76, 20.207237670000005],
                [1517086980, 1105.01, 1105.5, 1105.01, 1105.5, 30.242019230000004],
                [1517086920, 1105, 1105.01, 1105.01, 1105.01, 69.00462365],
                [1517086860, 1105, 1105.02, 1105.01, 1105.01, 6.90801848],
                [1517086800, 1104.49, 1105.49, 1104.88, 1105.49, 33.35358075],
                [1517086740, 1104.42, 1106, 1106, 1105.21, 39.70635478],
                [1517086680, 1102.35, 1104.9, 1103.14, 1104.9, 48.92473362000001],
                [1517086620, 1101.14, 1102, 1101.14, 1101.99, 86.99649130000003],
                [1517086560, 1099.25, 1101.13, 1099.39, 1101.13, 49.46366824],
                [1517086500, 1097, 1103.1, 1103.1, 1099.4, 79.80565315000001],
                [1517086440, 1103.83, 1109.15, 1109.15, 1103.83, 52.89331663000001],
                [1517086380, 1109.38, 1111.96, 1111.96, 1109.38, 41.92588497],
                [1517086320, 1108.78, 1115.11, 1115.11, 1111.99, 28.284292229999995],
                [1517086260, 1115.93, 1116.94, 1115.93, 1116.46, 43.78690950000001],
                [1517086200, 1115.92, 1115.93, 1115.93, 1115.92, 27.281441620000003],
                [1517086140, 1115.92, 1115.93, 1115.93, 1115.92, 22.841421349999997],
                [1517086080, 1115.9, 1115.99, 1115.91, 1115.93, 46.82612993000001],
                [1517086020, 1115.69, 1116.29, 1115.69, 1115.91, 74.31166118999998],
                [1517085960, 1114.23, 1116.5, 1114.23, 1115.7, 220.61855589999996],
                [1517085900, 1112.78, 1114.23, 1112.78, 1114.23, 33.29767464],
                [1517085840, 1112.78, 1113.48, 1113.48, 1112.79, 62.80732139999999],
                [1517085780, 1113.48, 1113.5, 1113.49, 1113.49, 28.33695255],
                [1517085720, 1113.31, 1113.5, 1113.32, 1113.49, 130.09613331000003],
                [1517085660, 1112.78, 1113.32, 1112.8, 1113.29, 145.75322325000002],
                [1517085600, 1112.8, 1113.3, 1112.81, 1113.29, 41.524558909999996],
                [1517085540, 1111.99, 1113.67, 1112, 1112.81, 50.46435099999999],
                [1517085480, 1111.39, 1112, 1111.39, 1112, 27.031470549999995],
                [1517085420, 1111.26, 1111.88, 1111.27, 1111.88, 134.77208092],
                [1517085360, 1111.26, 1111.27, 1111.27, 1111.27, 49.20366439000002],
                [1517085300, 1111.25, 1111.51, 1111.25, 1111.27, 54.748509459999994],
                [1517085240, 1110.96, 1111.5, 1110.96, 1111.25, 52.348959750000006],
                [1517085180, 1110, 1112.88, 1110.03, 1110.97, 54.80841285],
                [1517085120, 1109.23, 1112.88, 1109.23, 1110.87, 20.65835103],
                [1517085060, 1108.12, 1109, 1108.79, 1109, 23.960047909999997],
                [1517085000, 1107.99, 1108.8, 1108, 1108.8, 30.459690210000005],
                [1517084940, 1107.99, 1108, 1108, 1107.99, 78.70541170000001],
                [1517084880, 1107.99, 1108, 1107.99, 1107.99, 35.79207967999999],
                [1517084820, 1107.14, 1108, 1107.15, 1107.99, 43.93993508],
                [1517084760, 1107.14, 1108.09, 1107.99, 1107.15, 44.68191856],
                [1517084700, 1104.93, 1108, 1104.93, 1107.99, 58.55729881999999],
                [1517084640, 1104.5, 1104.93, 1104.5, 1104.93, 69.40842212999999],
                [1517084580, 1104.5, 1104.52, 1104.51, 1104.5, 58.91577748],
                [1517084520, 1104.5, 1104.52, 1104.51, 1104.52, 48.664457139999996],
                [1517084460, 1104.12, 1105.01, 1105, 1104.5, 39.498248860000004],
                [1517084400, 1105, 1106.6, 1106.6, 1105, 50.912056969999995],
                [1517084340, 1107.1, 1107.5, 1107.5, 1107.1, 43.12631616],
                [1517084280, 1107.5, 1108.1, 1108.09, 1107.5, 53.39445875999999],
                [1517084220, 1108.09, 1108.11, 1108.1, 1108.09, 48.27439623],
                [1517084160, 1108.1, 1108.82, 1108.1, 1108.22, 110.83013197999999],
                [1517084100, 1107.14, 1108.11, 1107.14, 1108.1, 64.41293123],
                [1517084040, 1107.03, 1107.55, 1107.03, 1107.15, 32.69767418],
                [1517083980, 1107, 1108, 1107.54, 1107.4, 46.277057039999995],
                [1517083920, 1104, 1107.99, 1104.23, 1107.99, 70.54486062000001],
                [1517083860, 1101.71, 1112.11, 1111.97, 1104.13, 137.47156938],
                [1517083800, 1107.4, 1111.97, 1107.41, 1111.97, 94.59341029],
                [1517083740, 1098.5, 1108, 1098.5, 1107.41, 116.87815864],
                [1517083680, 1095, 1097, 1095, 1097, 79.62901076000001],
                [1517083620, 1094.79, 1095, 1094.8, 1095, 57.104386730000016],
                [1517083560, 1094.49, 1094.79, 1094.53, 1094.7, 64.30512046999999],
                [1517083500, 1091.28, 1094.09, 1091.29, 1094.09, 25.249771169999995],
                [1517083440, 1091.25, 1094.8, 1094.79, 1091.29, 35.512989579999996],
                [1517083380, 1093, 1095, 1094.32, 1094.79, 44.395564019999995],
                [1517083320, 1093.37, 1094.32, 1093.38, 1094.32, 92.14932411999999],
                [1517083260, 1093, 1093.38, 1093, 1093.38, 52.42130352000001],
                [1517083200, 1091.78, 1092.2, 1091.79, 1092.2, 11.676599699999999],
                [1517083140, 1091.78, 1091.79, 1091.78, 1091.78, 7.22766841],
                [1517083080, 1091.78, 1091.79, 1091.79, 1091.78, 13.52912925],
                [1517083020, 1091.78, 1091.79, 1091.78, 1091.79, 21.14665742],
                [1517082960, 1090.99, 1091.81, 1091.8, 1091.79, 23.44577335],
                [1517082900, 1091.8, 1091.81, 1091.81, 1091.81, 9.67719997],
                [1517082840, 1091.8, 1091.81, 1091.81, 1091.81, 25.908036159999998],
                [1517082780, 1091, 1091.81, 1091, 1091.8, 13.353984489999998],
                [1517082720, 1090.99, 1091, 1090.99, 1090.99, 11.725334259999999],
                [1517082660, 1090.21, 1091, 1090.21, 1091, 32.46918128],
                [1517082600, 1089.99, 1090.21, 1089.99, 1090.21, 20.781384239999998],
                [1517082540, 1088.94, 1090, 1088.95, 1090, 220.25669288],
                [1517082480, 1088.95, 1088.95, 1088.95, 1088.95, 22.606351159999996],
                [1517082420, 1088.94, 1088.95, 1088.95, 1088.94, 49.101328699999996],
                [1517082360, 1088.94, 1088.95, 1088.95, 1088.95, 88.11420081],
                [1517082300, 1087.51, 1088.99, 1088.72, 1088.95, 18.79207514],
                [1517082240, 1088.1, 1089.98, 1089.98, 1088.15, 30.492837249999997],
                [1517082180, 1088.24, 1089.95, 1088.24, 1089.93, 12.6630191],
                [1517082120, 1086.49, 1088.25, 1086.49, 1088.25, 15.11811772],
                [1517082060, 1086.49, 1086.5, 1086.5, 1086.49, 43.822650759999995],
                [1517082000, 1086.37, 1086.5, 1086.37, 1086.5, 9.49151653],
                [1517081940, 1086.36, 1086.37, 1086.36, 1086.37, 14.860860899999999],
                [1517081880, 1086, 1086.71, 1086.71, 1086.36, 22.59580063],
                [1517081820, 1087, 1088, 1087.99, 1087, 31.21246042],
                [1517081760, 1087.48, 1088, 1087.48, 1088, 9.975417100000001],
                [1517081700, 1085.66, 1088, 1085.66, 1088, 14.173470509999998],
                [1517081640, 1085.37, 1085.67, 1085.38, 1085.67, 11.223057390000003],
                [1517081580, 1085.33, 1086.48, 1086.48, 1085.38, 3.6686139399999993],
                [1517081520, 1086.47, 1086.48, 1086.47, 1086.47, 23.170398940000005],
                [1517081460, 1085.33, 1088.54, 1087.92, 1086.48, 23.228808040000004],
                [1517081400, 1090.02, 1090.03, 1090.03, 1090.02, 9.949126719999999],
                [1517081340, 1090.02, 1091.55, 1091.55, 1090.02, 22.69383676],
                [1517081280, 1091.8, 1091.93, 1091.92, 1091.8, 16.74094907],
                [1517081220, 1091.92, 1091.93, 1091.93, 1091.93, 15.282941169999999],
                [1517081160, 1090, 1093.92, 1093.92, 1091.93, 9.422888959999998],
                [1517081100, 1093.53, 1093.99, 1093.54, 1093.63, 8.33047113],
                [1517081040, 1091.47, 1093.54, 1091.49, 1093.54, 12.318570730000001],
                [1517080980, 1090.02, 1094.89, 1094.89, 1090.03, 38.6200532],
                [1517080920, 1094.89, 1094.9, 1094.9, 1094.9, 5.571678809999999],
                [1517080860, 1093.49, 1094.77, 1093.49, 1094.77, 6.8264015],
                [1517080800, 1093.48, 1093.5, 1093.49, 1093.5, 16.317673879999997],
                [1517080740, 1093.48, 1093.49, 1093.48, 1093.49, 8.961066290000002],
                [1517080680, 1093.48, 1093.49, 1093.48, 1093.49, 11.57198883],
                [1517080620, 1093.18, 1093.49, 1093.18, 1093.48, 38.706268599999994],
                [1517080560, 1092.79, 1093.19, 1092.79, 1093.19, 88.27719399],
                [1517080500, 1091.99, 1092.8, 1091.99, 1092.8, 19.814010100000004],
                [1517080440, 1091.98, 1091.99, 1091.98, 1091.99, 20.89770828],
                [1517080380, 1091.98, 1091.99, 1091.99, 1091.98, 3.6946136],
                [1517080320, 1091.98, 1092, 1091.99, 1091.99, 11.539403759999999],
                [1517080260, 1091.99, 1092, 1092, 1091.99, 11.23121244],
                [1517080200, 1091.99, 1092, 1091.99, 1092, 3.92933272],
                [1517080140, 1091.99, 1092, 1092, 1092, 20.394070059999994],
                [1517080080, 1091.99, 1092, 1092, 1092, 33.089475969999995],
                [1517080020, 1092, 1092, 1092, 1092, 12.79995383],
                [1517079960, 1091.62, 1092, 1091.62, 1091.99, 7.834908369999998],
                [1517079900, 1089, 1091.62, 1089, 1091.62, 31.99313312],
                [1517079840, 1088.5, 1088.99, 1088.5, 1088.99, 23.671500800000004],
                [1517079780, 1088.5, 1088.51, 1088.51, 1088.5, 9.67209828],
                [1517079720, 1088.5, 1088.51, 1088.5, 1088.5, 17.489623350000002],
                [1517079660, 1088.5, 1088.51, 1088.51, 1088.51, 17.199420630000002],
                [1517079600, 1088.5, 1088.51, 1088.51, 1088.51, 18.99655031],
                [1517079540, 1088.5, 1088.51, 1088.5, 1088.51, 10.73040838],
                [1517079480, 1088.5, 1088.51, 1088.51, 1088.51, 4.38463802],
                [1517079420, 1088.5, 1088.83, 1088.83, 1088.5, 12.680098139999998],
                [1517079360, 1088.82, 1088.83, 1088.82, 1088.82, 5.511645039999999],
                [1517079300, 1088.82, 1088.83, 1088.82, 1088.82, 19.67260338],
                [1517079240, 1088.82, 1088.83, 1088.82, 1088.83, 9.75296023],
                [1517079180, 1088.71, 1088.88, 1088.88, 1088.82, 5.94185613],
                [1517079120, 1088.1, 1088.98, 1088.51, 1088.44, 58.01273926],
                [1517079060, 1088.5, 1088.92, 1088.92, 1088.5, 18.39374895],
                [1517079000, 1088.91, 1088.97, 1088.92, 1088.91, 22.08540052],
                [1517078940, 1088.91, 1088.92, 1088.91, 1088.92, 9.73063079],
                [1517078880, 1088.13, 1088.92, 1088.51, 1088.92, 13.17804709],
                [1517078820, 1088.14, 1088.78, 1088.52, 1088.51, 15.90515994],
                [1517078760, 1088.13, 1088.92, 1088.92, 1088.52, 2.7616923399999997],
                [1517078700, 1088.13, 1088.68, 1088.13, 1088.32, 10.707391139999999],
                [1517078640, 1088.01, 1089, 1088.01, 1089, 25.23612941],
                [1517078580, 1088.01, 1088.02, 1088.01, 1088.02, 16.220782200000002],
                [1517078520, 1088.01, 1088.03, 1088.03, 1088.02, 15.785553580000002],
                [1517078460, 1088, 1088.03, 1088.03, 1088.02, 11.73537368],
                [1517078400, 1088.02, 1088.04, 1088.03, 1088.03, 4.610742870000001],
                [1517078340, 1088.9, 1088.91, 1088.9, 1088.91, 20.18913991],
                [1517078280, 1088.9, 1090, 1089.99, 1088.9, 59.108011700000006],
                [1517078220, 1089.99, 1090, 1089.99, 1089.99, 8.66762615],
                [1517078160, 1089.99, 1090, 1089.99, 1089.99, 19.49162003],
                [1517078100, 1089, 1090, 1089.01, 1090, 10.4361644],
                [1517078040, 1089, 1089.01, 1089.01, 1089, 18.75183796],
                [1517077980, 1088, 1089, 1088.01, 1089, 47.00612336],
                [1517077920, 1088, 1088.01, 1088, 1088, 22.265328349999997],
                [1517077860, 1088, 1088.03, 1088.03, 1088, 19.42091674],
                [1517077800, 1088, 1090, 1089.99, 1088.02, 25.44777951],
                [1517077740, 1089.99, 1090, 1089.99, 1090, 9.61730579],
                [1517077680, 1089.99, 1090, 1089.99, 1090, 10.29556827],
                [1517077620, 1089.99, 1090, 1090, 1090, 2.1847338599999997],
                [1517077560, 1088.89, 1089.99, 1088.89, 1089.99, 14.06438153],
                [1517077500, 1088.29, 1088.89, 1088.29, 1088.88, 8.235200940000002],
                [1517077440, 1087.99, 1088.29, 1087.99, 1088.29, 28.686044319999993],
                [1517077380, 1086.99, 1088, 1086.99, 1088, 19.314613339999998],
                [1517077320, 1086.99, 1087, 1087, 1086.99, 11.034532749999999],
                [1517077260, 1086.88, 1086.89, 1086.88, 1086.88, 11.38626839],
                [1517077200, 1086.19, 1086.89, 1086.19, 1086.89, 15.72294407],
                [1517077140, 1083.99, 1086.2, 1084, 1086.2, 9.931216299999999],
                [1517077080, 1082.43, 1083.2, 1083.2, 1083.2, 13.55805561],
                [1517077020, 1083.18, 1083.2, 1083.19, 1083.19, 33.78715188],
                [1517076960, 1083.18, 1083.19, 1083.19, 1083.19, 14.438239519999998],
                [1517076900, 1083.15, 1083.19, 1083.15, 1083.19, 2.35022052],
                [1517076840, 1083.18, 1083.19, 1083.18, 1083.18, 27.747068940000002],
                [1517076780, 1083.18, 1083.19, 1083.18, 1083.18, 12.338616250000001],
                [1517076720, 1083.18, 1083.19, 1083.19, 1083.18, 11.237420460000001],
                [1517076660, 1083.18, 1083.19, 1083.18, 1083.19, 9.096737300000001],
                [1517076600, 1083.18, 1083.19, 1083.18, 1083.19, 29.65456787],
                [1517076540, 1083.18, 1084.01, 1084.01, 1083.18, 59.49756771],
                [1517076480, 1084.01, 1086.2, 1086.2, 1084.01, 16.120911149999998],
                [1517076420, 1086.19, 1086.2, 1086.2, 1086.2, 22.068839739999998],
                [1517076360, 1086.19, 1086.2, 1086.2, 1086.19, 47.23072562],
                [1517076300, 1086.19, 1086.2, 1086.19, 1086.2, 25.512445070000002],
                [1517076240, 1086.19, 1086.2, 1086.2, 1086.2, 23.211402300000003],
                [1517076180, 1086.19, 1086.2, 1086.2, 1086.19, 101.64641501],
                [1517076120, 1086.19, 1086.2, 1086.19, 1086.2, 24.4705864],
                [1517076060, 1086.19, 1086.2, 1086.2, 1086.2, 33.79990553],
                [1517076000, 1086.19, 1086.2, 1086.19, 1086.2, 33.10837826],
                [1517075940, 1086.19, 1086.2, 1086.19, 1086.2, 23.432993359999998],
                [1517075880, 1086.2, 1086.2, 1086.2, 1086.2, 38.7229688],
                [1517075820, 1086.19, 1086.2, 1086.19, 1086.19, 20.241931599999997],
                [1517075760, 1086.19, 1086.2, 1086.2, 1086.2, 44.75966039],
                [1517075700, 1084.99, 1086.2, 1084.99, 1086.2, 10.363835459999999],
                [1517075640, 1084.98, 1085, 1084.98, 1085, 31.796309830000006],
                [1517075580, 1083.49, 1084.99, 1083.5, 1084.99, 37.69338166999999],
                [1517075520, 1082.98, 1083.5, 1082.98, 1083.5, 25.889900869999998],
                [1517075460, 1082.03, 1082.98, 1082.04, 1082.98, 114.19939215],
                [1517075400, 1082.03, 1082.04, 1082.03, 1082.03, 15.702116610000001],
                [1517075340, 1082, 1082.22, 1082, 1082.04, 9.808260370000001],
                [1517075280, 1082.22, 1083.49, 1083.49, 1082.22, 15.279017740000002],
                [1517075220, 1080.87, 1083.99, 1083.99, 1083.5, 55.45130108000002],
                [1517075160, 1083.99, 1085.5, 1085.5, 1083.99, 29.193930189999996],
                [1517075100, 1086, 1086.05, 1086.04, 1086, 10.25639009],
                [1517075040, 1086.04, 1086.65, 1086.65, 1086.04, 16.64247436],
                [1517074980, 1086.65, 1091.01, 1091, 1086.65, 51.15253216000001],
                [1517074920, 1091, 1092, 1092, 1091, 25.56753773],
                [1517074860, 1091.99, 1092, 1091.99, 1091.99, 33.96836098],
                [1517074800, 1091.99, 1092, 1091.99, 1092, 15.43656947],
                [1517074740, 1091.99, 1092, 1092, 1092, 56.28855758],
                [1517074680, 1091.99, 1092, 1091.99, 1092, 5.33926225],
                [1517074620, 1091.99, 1092, 1092, 1091.99, 12.67754923],
                [1517074560, 1091.99, 1092, 1092, 1092, 6.24465769],
                [1517074500, 1091.99, 1092, 1091.99, 1092, 13.07741461],
                [1517074440, 1091.99, 1092, 1091.99, 1092, 14.91440758],
                [1517074380, 1091.41, 1093.58, 1093.58, 1091.99, 52.34074335000001],
                [1517074320, 1094.36, 1096.7, 1096.7, 1094.36, 45.83975784],
                [1517074260, 1096.7, 1096.72, 1096.71, 1096.7, 103.10500873999999],
                [1517074200, 1096.71, 1096.72, 1096.72, 1096.71, 29.927573019999997],
                [1517074140, 1096.71, 1096.72, 1096.71, 1096.71, 20.277261639999995],
                [1517074080, 1096.71, 1096.72, 1096.71, 1096.72, 50.1345267],
                [1517074020, 1096.71, 1096.72, 1096.71, 1096.72, 51.31918066],
                [1517073960, 1096.71, 1096.72, 1096.72, 1096.72, 64.99080787],
                [1517073900, 1096.71, 1096.72, 1096.71, 1096.71, 130.66003523],
                [1517073840, 1096.71, 1096.72, 1096.72, 1096.71, 19.3615043],
                [1517073780, 1096.71, 1096.73, 1096.73, 1096.72, 41.84627458],
                [1517073720, 1096.7, 1096.75, 1096.75, 1096.7, 64.89803004],
                [1517073660, 1094.49, 1096.74, 1094.5, 1096.74, 56.08888927000001],
                [1517073600, 1093.36, 1094.47, 1093.37, 1094.47, 32.25896786],
                [1517073540, 1092.91, 1093.37, 1092.91, 1093.36, 19.43901961],
                [1517073480, 1092.83, 1092.92, 1092.83, 1092.92, 32.974281489999996],
                [1517073420, 1091.01, 1092.92, 1091.01, 1092.83, 28.28632637],
                [1517073360, 1089.5, 1091, 1089.5, 1090.99, 36.376486670000006],
                [1517073300, 1089.49, 1089.5, 1089.49, 1089.49, 98.3876862],
                [1517073240, 1089.49, 1089.5, 1089.5, 1089.5, 34.03766977],
                [1517073180, 1089.02, 1089.5, 1089.02, 1089.5, 9.12374804],
                [1517073120, 1089, 1089.01, 1089.01, 1089.01, 108.84672763999997],
                [1517073060, 1089, 1089.01, 1089.01, 1089.01, 31.42295468],
                [1517073000, 1089, 1089.01, 1089.01, 1089.01, 10.547904180000002],
                [1517072940, 1089, 1089.01, 1089.01, 1089, 10.786968629999997],
                [1517072880, 1089, 1089.01, 1089, 1089, 19.65016136],
                [1517072820, 1087.26, 1093.02, 1093.02, 1089, 45.78630623999999],
                [1517072760, 1093.51, 1094, 1094, 1093.51, 47.41346756],
                [1517072700, 1092.99, 1094, 1093, 1093.99, 79.88932602000013],
                [1517072640, 1092.73, 1096.59, 1096.59, 1093, 91.30015552000002],
                [1517072580, 1096.51, 1096.59, 1096.51, 1096.59, 28.531436309999997],
                [1517072520, 1096.48, 1096.65, 1096.48, 1096.65, 27.496720840000002],
                [1517072460, 1095.99, 1096.49, 1095.99, 1096.49, 75.73299028999998],
                [1517072400, 1094.99, 1096, 1095, 1096, 47.216734699999996],
                [1517072340, 1094.43, 1094.93, 1094.44, 1094.93, 51.27572479],
                [1517072280, 1094.22, 1094.44, 1094.23, 1094.43, 42.53807581],
                [1517072220, 1092, 1094.15, 1092, 1094.14, 24.266354019999998],
                [1517072160, 1089.99, 1092, 1090, 1091.99, 103.77563452999999],
                [1517072100, 1089.47, 1090, 1089.47, 1090, 41.702896110000005],
                [1517072040, 1088.69, 1089.45, 1088.7, 1089.45, 10.998979550000001],
                [1517071980, 1087, 1088.42, 1087, 1088.42, 72.04927843],
                [1517071920, 1085.98, 1087, 1085.98, 1087, 22.806972740000006],
                [1517071860, 1084.45, 1085.96, 1085, 1085.96, 158.17566498000002],
                [1517071800, 1084.45, 1085, 1084.98, 1084.99, 116.89803938000001],
                [1517071740, 1084.36, 1084.9, 1084.36, 1084.9, 39.279520149999996],
                [1517071680, 1083.01, 1085, 1083.99, 1084.01, 29.3615192],
                [1517071620, 1083.01, 1085, 1083.02, 1083.59, 254.39402943000002],
                [1517071560, 1083.01, 1083.02, 1083.02, 1083.02, 34.09378145],
                [1517071500, 1083.01, 1083.02, 1083.02, 1083.02, 10.502810010000001],
                [1517071440, 1082.99, 1083.02, 1083, 1083.02, 10.8609907],
                [1517071380, 1082.99, 1083, 1083, 1082.99, 24.77354764],
                [1517071320, 1082.99, 1083, 1082.99, 1082.99, 42.07220963],
                [1517071260, 1081.99, 1083, 1081.99, 1083, 37.428382559999996],
                [1517071200, 1081.97, 1082, 1081.99, 1082, 39.816234140000006],
                [1517071140, 1081.99, 1082, 1082, 1082, 26.6451275],
                [1517071080, 1081.96, 1081.99, 1081.99, 1081.99, 17.96246932],
                [1517071020, 1081, 1082.01, 1081, 1081.51, 7.92627517],
                [1517070960, 1080.81, 1082.99, 1082.99, 1081.37, 106.50944014000002],
                [1517070900, 1082.98, 1084.04, 1084.03, 1082.99, 21.26627882],
                [1517070840, 1084.5, 1084.7, 1084.69, 1084.5, 12.56392477],
                [1517070780, 1083.86, 1084.7, 1083.86, 1084.69, 20.542347820000003],
                [1517070720, 1083.19, 1083.86, 1083.19, 1083.86, 6.135707480000001],
                [1517070660, 1083.19, 1083.2, 1083.2, 1083.2, 136.8199103],
                [1517070600, 1083.19, 1083.2, 1083.19, 1083.2, 50.6209742],
                [1517070540, 1083.19, 1083.2, 1083.2, 1083.2, 27.083876890000003],
                [1517070480, 1083.19, 1083.2, 1083.19, 1083.19, 7.9156248],
                [1517070420, 1083, 1083.2, 1083.01, 1083.2, 32.17516128],
                [1517070360, 1082.98, 1083.01, 1082.99, 1083.01, 5.060814730000001],
                [1517070300, 1081.99, 1082.99, 1082, 1082.99, 32.288077259999994],
                [1517070240, 1080.97, 1081.84, 1080.97, 1081.84, 9.66431397],
                [1517070180, 1080.42, 1080.97, 1080.42, 1080.96, 22.60343041],
                [1517070120, 1080.4, 1080.42, 1080.41, 1080.41, 111.36598633000001],
                [1517070060, 1080.4, 1080.41, 1080.41, 1080.4, 54.145507980000005],
                [1517070000, 1080.3, 1080.41, 1080.41, 1080.41, 166.67426011000003],
                [1517069940, 1080, 1080.72, 1080.01, 1080.4, 59.06422759],
                [1517069880, 1080.22, 1080.75, 1080.22, 1080.74, 44.819323250000004],
                [1517069820, 1080, 1082.01, 1082.01, 1080, 32.64514327],
                [1517069760, 1082, 1082.27, 1082.27, 1082.01, 13.58618104],
                [1517069700, 1080.01, 1082.54, 1080.01, 1082.28, 61.983008670000004],
                [1517069640, 1080.6, 1082.97, 1082.97, 1080.6, 43.072313949999995],
                [1517069580, 1081.51, 1083.01, 1083, 1082.97, 33.98789031],
                [1517069520, 1083, 1084.88, 1084.87, 1083, 39.47414316],
                [1517069460, 1084.87, 1084.88, 1084.87, 1084.87, 47.72034388000001],
                [1517069400, 1084.87, 1084.88, 1084.87, 1084.87, 59.217081590000014],
                [1517069340, 1084.87, 1084.88, 1084.88, 1084.87, 118.7814654],
                [1517069280, 1084.87, 1084.88, 1084.88, 1084.88, 43.962901939999995],
                [1517069220, 1084.87, 1084.88, 1084.88, 1084.88, 36.358126299999995],
                [1517069160, 1084.87, 1084.88, 1084.88, 1084.88, 58.01772887],
                [1517069100, 1084.2, 1084.88, 1084.2, 1084.88, 49.53076765000001],
                [1517069040, 1082.61, 1084.1, 1083.42, 1084.1, 34.13394600000001],
                [1517068980, 1079.01, 1085, 1079.02, 1084.65, 118.86668688000002],
                [1517068920, 1079.01, 1079.3, 1079.3, 1079.02, 32.64551618],
                [1517068860, 1079.61, 1083.19, 1083.16, 1080.64, 41.65281563999999],
                [1517068800, 1082.88, 1086.01, 1086.01, 1082.88, 40.83597133999999],
                [1517068740, 1086.01, 1087.77, 1087.76, 1086.01, 91.61788870999999],
                [1517068680, 1086.99, 1088.3, 1087, 1087.87, 71.74310045],
                [1517068620, 1086.99, 1087, 1087, 1087, 9.74795564]
        ]
