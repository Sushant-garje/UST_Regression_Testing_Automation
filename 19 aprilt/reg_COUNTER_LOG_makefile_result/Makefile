SIM = vcs

RTL = rtl/counter.sv
TB  = rtl/env.sv \
      rtl/counter_interface.sv \
      rtl/tb_top.sv

compile:
	$(SIM) -full64 -sverilog $(RTL) $(TB) -o simv

run:
	./simv +seed=1 +tests=100

regress:
	mkdir -p logs results waves
	@for i in 1 2 3 4 5; do \
		echo Running Seed $$i; \
		./simv +testname=regression_counter +seed=$$i | tee logs/run_$$i.log; \
	done

clean:
	rm -rf simv simv.daidir csrc *.log logs results waves DVEfiles ucli.key
