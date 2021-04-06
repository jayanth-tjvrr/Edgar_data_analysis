# Edgar_data_analysis
Data Extraction and Text Analysis of Financial Reports

** Objective of this assignment is to extract some sections (which are mentioned below) from SEC / EDGAR financial reports and perform text analysis to compute variables those are explained below. Link to SEC / EDGAR financial reports are given in excel spreadsheet “cik_list.xlsx”. Please add https://www.sec.gov/Archives/ to every cells of column F (cik_list.xlsx) to access link to the financial report.
Example: Row 2, column F contains edgar/data/3662/0000950170-98-000413.txt
Add https://www.sec.gov/Archives/ to form financial report link
i.e. https://www.sec.gov/Archives/edgar/data/3662/0000950170-98-000413.txt

“Management's Discussion and Analysis”: MDA
“Quantitative and Qualitative Disclosures about Market Risk”: QQDMR
“Risk Factors”: RF

The output dataframe should contain: 

1. All input variables in “cik_list.xlsx”
2. mda_positive_score
3. mda_negative_score
4. mda_polarity_score
5. mda_average_sentence_length
6. mda_percentage_of_complex_words
7. mda_fog_index
8. mda_complex_word_count
9. mda_word_count
10. mda_uncertainty_score
11. mda_constraining_score
12. mda_positive_word_proportion
13. mda_negative_word_proportion
14. mda_uncertainty_word_proportion
15. mda_constraining_word_proportion
16. qqdmr_positive_score
17. qqdmr_negative_score
18. qqdmr_polarity_score
19. qqdmr_average_sentence_length
20. qqdmr_percentage_of_complex_words
21. qqdmr_fog_index
22. qqdmr_complex_word_count
23. qqdmr_word_count
24. qqdmr_uncertainty_score
25. qqdmr_constraining_score
26. qqdmr_positive_word_proportion
27. qqdmr_negative_word_proportion
28. qqdmr_uncertainty_word_proportion
29. qqdmr_constraining_word_proportion
30. rf_positive_score
31. rf_negative_score
32. rf_polarity_score
33. rf_average_sentence_length
34. rf_percentage_of_complex_words
35. rf_fog_index
36. rf_complex_word_count
37. rf_word_count
38. rf_uncertainty_score
39. rf_constraining_score
40. rf_positive_word_proportion
41. rf_negative_word_proportion
42. rf_uncertainty_word_proportion
43. rf_constraining_word_proportion
44. constraining_words_whole_report

Checkout output data structure spreadsheet for format of your output.
