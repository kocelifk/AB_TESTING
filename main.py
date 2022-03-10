
# Gerekli Kütüphanelerin Yüklenmesi
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import shapiro, ttest_ind
import scipy.stats as stats
pd.set_option('display.max_columns', None)

Control_Group = pd.read_excel("datasets/ab_testing.xlsx", sheet_name='Control Group')  # maximum bidding
Control_Group.head()
Control_Group.shape
Control_Group.isnull().sum()
Control_Group.describe([0.90,0.95,0.99]).T


Test_Group = pd.read_excel("datasets/ab_testing.xlsx", sheet_name='Test Group') # average bidding
Test_Group.head()
Test_Group.shape
Test_Group.isnull().sum()
Test_Group.describe([0.90,0.95,0.99]).T


######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.



print(" Mean of purchase of control group: %.3f"%Control_Group["Purchase"].mean(),"\n",
      "Mean of purchase of test group: %.3f"%Test_Group["Purchase"].mean())

groupA = Control_Group["Purchase"]
groupB = Test_Group["Purchase"]

############################
# 2. Varsayım Kontrolü
############################

# 1. Normallik Varsayımı
# veri setinde medyan değerin ve ortalamanın birbirine çok yakın olması durumudur.
# Yani verilerin çoğunluğu ortalama değer/medyan etrafında kümelenir ve bir tepecik oluşturur.
# Grafiğin simetrik olması en önemli özelliğidir.


# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.


test_istatistigi, pvalue = shapiro(groupA)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# Normal dağılım sağlanmakta

test_istatistigi, pvalue = shapiro(groupB)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# Normal dağılım sağlanmakta


# 2. Varyans Homojenliği
# İki grubun dağılımlarının birbirine benzer olup olmaması

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_istatistigi, pvalue = stats.levene(groupA,groupB)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# Varyanslar homejendir.



############################
# Hipotezin Uygulanması
############################

# Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)

test_stat, pvalue = ttest_ind(groupA,groupB,equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# P değeri 0,05'ten büyük olduğundan H0 reddedilmez. Dolayısıyla, “maksimum teklif” kampanyası sunulan Kontrol grubu ile
# “ortalama teklif” kampanyası sunulan Test grubu arasında istatistiksel olarak anlamlı bir fark yoktur.


############################
#Hangi testi kullandınız? Neden?
############################

# Bağımsız t-testi kullandık çünkü birbirinden bağımsız  iki grubun ortalamaları arasında
# belirli özelliklerde ilişkili olabilecek anlamlı bir fark olup olmadığını belirlemek istiyoruz ve varsayımlara
# sonucunda iki grubunda normal dağılımave varyans homojenliğine sahip olduğunu gördük.


############################
#Müşteriye tavsiyeniz nedir?
############################

# Satın alma anlamında anlamlı bir fark olmadığından müşteri iki yöntemden birini seçebilir fakat burada
# diğer istatistiklerdeki farklılıklar da önem arz edecektir. Tıklanma, Etkileşim, Kazanç ve Dönüşüm Oranlarındaki
# farklılıklar değerlendirilip hangi yöntemin daha kazançlı olduğu tespit edilebilir.

