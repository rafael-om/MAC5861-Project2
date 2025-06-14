db.pessoas.createIndex({ name: "text" });
db.pessoas.createIndex({ age: 1 });
db.pessoas.createIndex({ wage: 1 });
db.pessoas.createIndex({ house_location_sphere: "2dsphere" });
db.pessoas.createIndex({ house_location_plane: "2d" });
db.pessoas.createIndex({ birth_date: 1 });
db.pessoas.createIndex({ cellphones: 1 });
db.pessoas.createIndex({ products_prices: 1 });
db.pessoas.createIndex({ wage: 1, old_wage: 1 });

//#region 1. name 
// Com índice simples
db.pessoas.find({ name: "João Silva" });
db.pessoas.find({ name: "Maria Oliveira" });
db.pessoas.find({ name: "Carlos Eduardo Souza" });
db.pessoas.find({ name: "Ana Beatriz Lima" });
db.pessoas.find({ name: "José Carlos Mendes" });
db.pessoas.find({ name: "Paula Fernanda Ribeiro" });
db.pessoas.find({ name: "Luiz Henrique Martins" });
db.pessoas.find({ name: "Fernanda da Silva" });
db.pessoas.find({ name: "Ricardo Almeida" });
db.pessoas.find({ name: "Camila dos Santos" });
// Com índice text
db.pessoas.find({ $text: { $search: "\"João Silva\"" } });
db.pessoas.find({ $text: { $search: "\"Maria Oliveira\"" } });
db.pessoas.find({ $text: { $search: "\"Carlos Eduardo Souza\"" } });
db.pessoas.find({ $text: { $search: "\"Ana Beatriz Lima\"" } });
db.pessoas.find({ $text: { $search: "\"José Carlos Mendes\"" } });
db.pessoas.find({ $text: { $search: "\"Paula Fernanda Ribeiro\"" } });
db.pessoas.find({ $text: { $search: "\"Luiz Henrique Martins\"" } });
db.pessoas.find({ $text: { $search: "\"Fernanda da Silva\"" } });
db.pessoas.find({ $text: { $search: "\"Ricardo Almeida\"" } });
db.pessoas.find({ $text: { $search: "\"Camila dos Santos\"" } });
// Com índice text - consultas específicas
db.pessoas.find({ $text: { $search: "João" } });
db.pessoas.find({ $text: { $search: "Silva" } });
db.pessoas.find({ $text: { $search: "Carlos" } });
db.pessoas.find({ $text: { $search: "Maria Souza" } });
db.pessoas.find({ $text: { $search: "\"André Luiz\"" } });
db.pessoas.find({ $text: { $search: "Camila Fernandes" } });
db.pessoas.find({ $text: { $search: "\"Carlos Henrique\"" } });
db.pessoas.find({ $text: { $search: "José Maria" } });
// Sem índice (usando regex)
db.pessoas.find({ name: { $regex: "\\bJoão\\b", $options: "i" } });
db.pessoas.find({ name: { $regex: "\\bSilva\\b", $options: "i" } });
db.pessoas.find({ name: { $regex: "\\bCarlos\\b", $options: "i" } });
db.pessoas.find({ name: { $regex: "\\bMaria\\b|\\bSouza\\b", $options: "i" } });
db.pessoas.find({ name: { $regex: "\\bAndré Luiz\\b", $options: "i" } });
db.pessoas.find({ name: { $regex: "\\bCamila\\b|\\bFernandes\\b", $options: "i" } });
db.pessoas.find({ name: { $regex: "\\bCarlos Henrique\\b", $options: "i" } });
db.pessoas.find({ name: { $regex: "\\bJosé\\b|\\bMaria\\b", $options: "i" } });
//#endregion

//#region 2. age
// Com índice
db.pessoas.find({ age: { $gt: 20 } });
db.pessoas.find({ age: { $gte: 70, $lte: 80 } });
db.pessoas.find({ age: { $lte: 90 } });
db.pessoas.find({ age: 0 });
db.pessoas.find({ age: 4 });
db.pessoas.find({ age: 18 });
db.pessoas.find({ age: 21 });
db.pessoas.find({ age: 32 });
db.pessoas.find({ age: 60 });
db.pessoas.find({ age: 110 });
// Sem índice
db.pessoas.find({ age: { $gt: 20 } }).hint({ $natural: 1 });
db.pessoas.find({ age: { $gte: 70, $lte: 80 } }).hint({ $natural: 1 });
db.pessoas.find({ age: { $lte: 90 } }).hint({ $natural: 1 });
db.pessoas.find({ age: 0 }).hint({ $natural: 1 });
db.pessoas.find({ age: 4 }).hint({ $natural: 1 });
db.pessoas.find({ age: 18 }).hint({ $natural: 1 });
db.pessoas.find({ age: 21 }).hint({ $natural: 1 });
db.pessoas.find({ age: 32 }).hint({ $natural: 1 });
db.pessoas.find({ age: 60 }).hint({ $natural: 1 });
db.pessoas.find({ age: 110 }).hint({ $natural: 1 });
//#endregion

//#region 3. wage
// Com índice
db.pessoas.find({ wage: { $gte: 2000, $lte: 2001 } });
db.pessoas.find({ wage: { $gte: 3000, $lte: 4001 } });
db.pessoas.find({ wage: { $gte: 30000, $lte: 50000 } });
db.pessoas.find({ wage: { $lte: 100 } });
db.pessoas.find({ wage: { $lte: 25000 } });
db.pessoas.find({ wage: { $gt: 20000 } });
// Sem índice
db.pessoas.find({ wage: { $gte: 2000, $lte: 2001 } }).hint({ $natural: 1 });
db.pessoas.find({ wage: { $gte: 3000, $lte: 4001 } }).hint({ $natural: 1 });
db.pessoas.find({ wage: { $gte: 30000, $lte: 50000 } }).hint({ $natural: 1 });
db.pessoas.find({ wage: { $lte: 100 } }).hint({ $natural: 1 });
db.pessoas.find({ wage: { $lte: 25000 } }).hint({ $natural: 1 });
db.pessoas.find({ wage: { $gt: 20000 } }).hint({ $natural: 1 });
//#endregion    

//#region 4. house_location_sphere
// Com índice near
db.pessoas.find({
  house_location_sphere: {
    $near: { $geometry: { type: "Point", coordinates: [-46.8603, -23.5231] }, $maxDistance: 200000 }
  }
});
db.pessoas.find({
  house_location_sphere: {
    $near: { $geometry: { type: "Point", coordinates: [-46.8603, -23.5231] }, $maxDistance: 1000000 }
  }
});
db.pessoas.find({
  house_location_sphere: {
    $near: { $geometry: { type: "Point", coordinates: [-46.8603, -23.5231] }, $maxDistance: 5000000 }
  }
});
// Com índice geoWithin
db.pessoas.find({
  house_location_sphere: {
    $geoWithin: { $centerSphere: [[-46.6532, -23.5874], 200 / 6378.1] }
  }
});
db.pessoas.find({
  house_location_sphere: {
    $geoWithin: { $centerSphere: [[-46.6532, -23.5874], 1000 / 6378.1] }
  }
});
db.pessoas.find({
  house_location_sphere: {
    $geoWithin: { $centerSphere: [[-46.6600, -23.6000], 5000 / 6378.1] }
  }
});
db.pessoas.find({
  house_location_sphere: {
    $geoWithin: { $box: [[-72.6700, -23.4800], [-46.6200, -3.4600]] }
  }
});
db.pessoas.find({
  house_location_sphere: {
    $geoWithin: { $geometry: { type: "Polygon", coordinates: [[
          [-46.6500, -3.5500],
          [-72.6400, -3.5500],
          [-72.6400, -23.5400],
          [-46.6500, -23.5400],
          [-46.6500, -3.5500]
        ]] } }
  }
});
// Sem índice
db.pessoas.find({
  $expr: {
    $lte: [
      { $multiply: [ 
        { $acos: { $add: [
            {
              $multiply: [
                { $sin: { $degreesToRadians: -23.5231 } },
                { $sin: { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 1] } } }
              ]
            },
            {
              $multiply: [
                { $cos: { $degreesToRadians: -23.5231 } },
                { $cos: { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 1] } } },
                { $cos: { $subtract: [
                      { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 0] } },
                      { $degreesToRadians: -46.8603 }
                    ]
                }}
              ]
            }
        ]}},
        6371000
      ]},
      200000
    ]
  }
});
db.pessoas.find({
  $expr: {
    $lte: [
      { $multiply: [ 
        { $acos: { $add: [
            {
              $multiply: [
                { $sin: { $degreesToRadians: -23.5231 } },
                { $sin: { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 1] } } }
              ]
            },
            {
              $multiply: [
                { $cos: { $degreesToRadians: -23.5231 } },
                { $cos: { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 1] } } },
                { $cos: { $subtract: [
                      { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 0] } },
                      { $degreesToRadians: -46.8603 }
                    ]
                }}
              ]
            }
        ]}},
        6371000
      ]},
      1000000
    ]
  }
});
db.pessoas.find({
  $expr: {
    $lte: [
      { $multiply: [ 
        { $acos: { $add: [
            {
              $multiply: [
                { $sin: { $degreesToRadians: -23.5231 } },
                { $sin: { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 1] } } }
              ]
            },
            {
              $multiply: [
                { $cos: { $degreesToRadians: -23.5231 } },
                { $cos: { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 1] } } },
                { $cos: { $subtract: [
                      { $degreesToRadians: { $arrayElemAt: ["$house_location_sphere.coordinates", 0] } },
                      { $degreesToRadians: -46.8603 }
                    ]
                }}
              ]
            }
        ]}},
        6371000
      ]},
      5000000
    ]
  }
});
//#endregion

//#region 5. house_location_plane
// Com índice near
db.pessoas.find({
  house_location_plane: { $near: [-46.8603, -23.5231], $maxDistance: 200 / 111.32 }
});
db.pessoas.find({
  house_location_plane: { $near: [-46.8603, -23.5231], $maxDistance: 1000 / 111.32 }
});
db.pessoas.find({
  house_location_plane: { $near: [-46.8603, -23.5231], $maxDistance: 5000 / 111.32 }
});
// Com índice geoWithin
db.pessoas.find({
  house_location_plane: {
    $geoWithin: { $center: [[-46.633309, -23.55052], 200 / 111.32] }
  }
});
db.pessoas.find({
  house_location_plane: {
    $geoWithin: { $center: [[-46.633309, -23.55052], 1000 / 111.32] }
  }
});
db.pessoas.find({
  house_location_plane: {
    $geoWithin: { $center: [[-46.6525, -23.5614], 5000 / 111.32] }
  }
});
db.pessoas.find({
  house_location_plane: {
    $geoWithin: { $box: [[-72.6700, -23.4800], [-46.6200, -3.4600]] }
  }
});
db.pessoas.find({
  house_location_plane: {
    $geoWithin: { $polygon: [
        [-46.6500, -3.5500],
        [-72.6400, -3.5500],
        [-72.6400, -23.5400],
        [-46.6500, -23.5400],
        [-46.6500, -3.5500]
      ] }
  }
});
// Sem índice
db.pessoas.find({
  $expr: { $lte: [
    { $sqrt: { $add: [
        { $pow: [{ $subtract: [{ $arrayElemAt: ["$house_location_plane", 0] }, -46.8603] }, 2] },
        { $pow: [{ $subtract: [{ $arrayElemAt: ["$house_location_plane", 1] }, -23.5231] }, 2] }
    ]}},
    200 / 111.32
  ]}
});
db.pessoas.find({
  $expr: { $lte: [
    { $sqrt: { $add: [
        { $pow: [{ $subtract: [{ $arrayElemAt: ["$house_location_plane", 0] }, -46.8603] }, 2] },
        { $pow: [{ $subtract: [{ $arrayElemAt: ["$house_location_plane", 1] }, -23.5231] }, 2] }
    ]}},
    1000 / 111.32
  ]}
});
db.pessoas.find({
  $expr: { $lte: [
    { $sqrt: { $add: [
        { $pow: [{ $subtract: [{ $arrayElemAt: ["$house_location_plane", 0] }, -46.8603] }, 2] },
        { $pow: [{ $subtract: [{ $arrayElemAt: ["$house_location_plane", 1] }, -23.5231] }, 2] }
    ]}},
    5000 / 111.32
  ]}
});
//#endregion

//#region 6. birth_date
// Com índice
db.pessoas.find({ birth_date: { $lt: ISODate("1950-01-01T00:00:00Z") } });
db.pessoas.find({ birth_date: { $gt: ISODate("2000-01-01T00:00:00Z") } });
db.pessoas.find({ birth_date: { $gt: ISODate("1990-01-01T00:00:00Z") } });
db.pessoas.find({ birth_date: { $lt: ISODate("1970-01-01T00:00:00Z") } });
// Sem índice
db.pessoas.find({ birth_date: { $lt: ISODate("1950-01-01T00:00:00Z") } }).hint({ $natural: 1 });
db.pessoas.find({ birth_date: { $gt: ISODate("2000-01-01T00:00:00Z") } }).hint({ $natural: 1 });
db.pessoas.find({ birth_date: { $gt: ISODate("1990-01-01T00:00:00Z") } }).hint({ $natural: 1 });
db.pessoas.find({ birth_date: { $lt: ISODate("1970-01-01T00:00:00Z") } }).hint({ $natural: 1 });
//#endregion

//#region 7. description 
// Com índice
db.pessoas.dropIndex("name_text");
db.pessoas.createIndex({ description: "text" });
db.pessoas.find({ $text: { $search: "wireless" } });
db.pessoas.find({ $text: { $search: "portable" } });
db.pessoas.find({ $text: { $search: "fast" } });
db.pessoas.find({ $text: { $search: "Bluetooth" } });
db.pessoas.find({ $text: { $search: "USB cable" } });
db.pessoas.find({ $text: { $search: "battery -replaceable" } });
db.pessoas.find({ $text: { $search: "wage money economy" } });
db.pessoas.find({ $text: { $search: "touchscreen" } });
db.pessoas.find({ $text: { $search: "touch" } });
db.pessoas.find({ $text: { $search: "name age" } });

// Sem índice
db.pessoas.find({ description: { $regex: "\\bwireless\\b", $options: "i" } });
db.pessoas.find({ description: { $regex: "\\bportable\\b", $options: "i" } });
db.pessoas.find({ description: { $regex: "\\bfast\\b", $options: "i" } });
db.pessoas.find({ description: { $regex: "\\bBluetooth\\b", $options: "i" } });
db.pessoas.find({ description: { $regex: "\\bUSB\\b|\\bcable\\b", $options: "i" } });
db.pessoas.find({
  $and: [
    { description: { $regex: "\\bwage\\b", $options: "i" } },
    { description: { $not: { $regex: "\\bmoney\\b", $options: "i" } } }
  ]
});
db.pessoas.find({ description: { $regex: "\\bwage\\b|\\bmoney\\b|\\beconomy\\b", $options: "i" } });
db.pessoas.find({ description: { $regex: "\\btouchscreen\\b", $options: "i" } });
db.pessoas.find({ description: { $regex: "\\btouch\\b", $options: "i" } });
db.pessoas.find({ description: { $regex: "\\bname\\b|\\bage\\b", $options: "i" } });
//#endregion

//#region 8. cellphones
// Com índice
db.pessoas.find({ cellphones: 5511987654321 });
db.pessoas.find({
  cellphones: { $gte: 31990000000, $lte: 31999999999 }
});
db.pessoas.find({
  cellphones: { $gt: 551290000000 }
});
db.pessoas.find({ cellphones: 71991234567 });

// Sem índice
db.pessoas.find({ cellphones: 5511987654321 }).hint({ $natural: 1 });
db.pessoas.find({
  cellphones: { $gte: 31990000000, $lte: 31999999999 }
}).hint({ $natural: 1 });
db.pessoas.find({
  cellphones: { $gt: 551290000000 }
}).hint({ $natural: 1 });
db.pessoas.find({ cellphones: 71991234567 }).hint({ $natural: 1 });
//#endregion

//#region 9. products_prices
// Com índice
db.pessoas.find({ products_prices: 199.99 });
db.pessoas.find({ products_prices: { $gt: 1000 } });
db.pessoas.find({ products_prices: { $gte: 500, $lte: 1500 } });
db.pessoas.find({ products_prices: { $lt: 50 } });

// Sem índice
db.pessoas.find({ products_prices: 199.99 }).hint({ $natural: 1 });
db.pessoas.find({ products_prices: { $gt: 1000 } }).hint({ $natural: 1 });
db.pessoas.find({ products_prices: { $gte: 500, $lte: 1500 } }).hint({ $natural: 1 });
db.pessoas.find({ products_prices: { $lt: 50 } }).hint({ $natural: 1 });
//#endregion

//#region 10. Indice composto wage e old_wage
// Com índice
db.pessoas.find({
  $expr: { $gt: ["$wage", "$old_wage"] }
});
db.pessoas.find({
  $expr: { $lt: ["$wage", "$old_wage"] }
});
db.pessoas.find({
  $expr: { $eq: ["$wage", "$old_wage"] }
});
db.pessoas.find({ wage: 5000.00, old_wage: 4500.00 });

// Sem índice
db.pessoas.find({
  $expr: { $gt: ["$wage", "$old_wage"] }
}).hint({ $natural: 1 });
db.pessoas.find({
  $expr: { $lt: ["$wage", "$old_wage"] }
}).hint({ $natural: 1 });
db.pessoas.find({
  $expr: { $eq: ["$wage", "$old_wage"] }
}).hint({ $natural: 1 });
db.pessoas.find({ wage: 5000.00, old_wage: 4500.00 }).hint({ $natural: 1 });
//#endregion
