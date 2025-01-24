import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
import pandas as pd
#Decídi eliminar los warnings ya que me generabán muchas líneas de código, afectando a la legilibilidad final

#Extraigo el CVS que quiero leer. Lo formateo como yo quiero, valores de fecha comprendidas entre el 2021 y 2022, y asigno nombre a un nuevo dataframe como df_filtrado
df = pd.read_csv(r'data//')
df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d-%m-%Y')
df_2021_2022 = ((df.invoice_date >='01-01-2021') & (df.invoice_date <= '31-12-2022'))
df_filtrado = df[df_2021_2022]
df_filtrado['invoice_date'] = df_filtrado['invoice_date'].dt.normalize()

#Armo una nueva columna que incluya las Ventas = price*quantity
df_filtrado['ventas'] = df_filtrado['quantity'] * df_filtrado['price']

#1. Busco el total de ingresos registrado en todos los centros comerciales
total_ingresos = df_filtrado['ventas'].sum()
print(f'1. El total de ingreso por ventas registradas es {total_ingresos:,.2f} USD')

#2. Busco el centro comercial con mayor ventas registradas
centro_comercial_mas_ventas = df_filtrado.groupby('shopping_mall')['ventas'].sum().sort_values(ascending=False)
print(f'2. El centro comercial que mas ventas a generado es {centro_comercial_mas_ventas.index[0]} con {centro_comercial_mas_ventas[0]:,.2f} USD')

#3. Busco la categoría que ha generado más ventas 
categoria_mas_vendida = df_filtrado.groupby('category')['ventas'].sum().sort_values(ascending=False)
print(f'3. La categoria más vendida es {categoria_mas_vendida.index[0]} con {categoria_mas_vendida[0]:,.2f} USD')

# 4. Busco el producto más caro que vendo 
categoria_producto_mas_caro = df_filtrado.groupby('category')['price'].max().sort_values(ascending=False)
print(f'4. El producto más caro vendido es {categoria_producto_mas_caro.index[0]} a precio de {categoria_producto_mas_caro[0]:,.2f} USD')

#5. Buscar cual es la factura que más antigua tengo registrada en mi sistema
factura_mas_antigua = df_filtrado.groupby('invoice_date').first().sort_index()['invoice_no']
print(f'5. La factura más antigua es la {factura_mas_antigua.iloc[0]} con fecha {factura_mas_antigua.index[0].strftime('%Y-%m-%d')}')

#6. Cuanto es la cantidad promedio de productos vendidos por transacción
cantidad_promedio_por_transaccion = df_filtrado['quantity'].mean()
print(f'6. La cantidad promedio de productos vendidos es {round(cantidad_promedio_por_transaccion)} unidades')

#Cual es el día que mayor cantidad de transacciones registró
dia_con_mas_ventas = df_filtrado['invoice_date'].value_counts()
print(f"7. El día con más registros fue el {dia_con_mas_ventas.index[0].strftime('%Y-%m-%d')}, con un total de {dia_con_mas_ventas.iloc[0]} transacciones")

#En caso de que sea otro el resultado, revisar las anotaciones siguientes
#7.a. Cual es el día que generó mayores ingresos por ventas 
# dia_con_mas_ventas = df_filtrado.groupby('invoice_date')['ventas'].sum().sort_values(ascending=False)
# print(f"7.a. El día con mayor ingresos por ventas fue el {dia_con_mas_ventas.index[0].strftime('%Y-%m-%d')}, con un total de {dia_con_mas_ventas.iloc[0]:,.2f} USD")

#7.b. Ahora bien, también podemos buscar aquel día que mayor cantidad de unidades fueron vendidas
# dia_con_mas_ventas = df_filtrado.groupby('invoice_date')['quantity'].sum().sort_values(ascending=False)
# print(f"7.b. El día con mayor cantidad de unidades vendidas fue el {dia_con_mas_ventas.index[0].strftime('%Y-%m-%d')}, con un total de {dia_con_mas_ventas.iloc[0]} unidades vendidas")

#8. Cuál es el cliente que más ha gastado
cliente_que_mas_gasto = df_filtrado.groupby('customer_id')['ventas'].max().sort_values(ascending=False)
print(f'8. El cliente que más gastó está registrado con el ID {cliente_que_mas_gasto.index[0]} gastando {cliente_que_mas_gasto.iloc[0]:,.2f} USD')

#9. Aquella factura que tiene mayor valor vendido
factura_max_valor = df_filtrado.groupby('invoice_no')['ventas'].max().sort_values(ascending=False)
print(f'9. La factura con precio más alto es la {factura_max_valor.index[0]} por un valor de {factura_max_valor.iloc[0]:,.2f} USD')

#10. Cómo se distribuyeron mis ventas en base a categoría de producto en términos porcentuales
ventas_por_categoria = df_filtrado.groupby('category')['ventas'].sum().sort_values(ascending=False)
distribucion_porcentual_ventas_por_categoria = ((ventas_por_categoria / ventas_por_categoria.sum()) * 100)
print(f'10. En la tabla de abajo se muestra la distribución porcentual de ventas por categoría: \n{distribucion_porcentual_ventas_por_categoria.map('{:.2f}%'.format)}')

#11. Qué día de la semana cada centros comerciales tienen mayores ventas?
dia_semana = df_filtrado['invoice_date'].apply(lambda x: x.day_name())
ventas_por_dia = df_filtrado.groupby(['shopping_mall',dia_semana])['ventas'].sum()
dia_semana_mas_ventas_por_centro = ventas_por_dia.groupby('shopping_mall').idxmax().apply(lambda x: x[1])
print(f'11. En la tabla de abajo se muestra el día de la semana con más ventas por centro comercial: \n{dia_semana_mas_ventas_por_centro}')