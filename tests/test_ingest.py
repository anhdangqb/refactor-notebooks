from src.ingest import remove_null, treat_outlier_df, treat_outlier_series


class TestRemoveNull:
    def test_remove_null_1_col(self, data_with_null):
        df = remove_null(data_with_null, ["CustomerID"])
        assert df.shape[0] == 2

    def test_remove_null_multiple_cols(self, data_with_null):
        df = remove_null(data_with_null, ["CustomerID", "Quantity"])
        assert df.shape[0] == 1

    # TODO: Add test for exception


class TestTreatOutlierSeries:
    def test_treat_outlier_series_cap(self, data_with_outliers):
        s = treat_outlier_series(data_with_outliers["Quantity"], [0, 20])
        assert s.max() == 20

    # TODO: Add test for floor


class TestTreatOutlierDF:
    def test_treat_outlier_df(self, data_with_outliers, outlier_policies):
        df = treat_outlier_df(data_with_outliers, outlier_policies)
        assert df["Quantity"].max() <= 40
        assert df["UnitPrice"].max() <= 5
